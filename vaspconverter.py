#!/usr/bin/env python3
"""Convert a set of VASP input files into gpawsolve-ready inputs.

The script reads VASP style POSCAR/CONTCAR (structure), INCAR (calculation
parameters) and KPOINTS files and gives:
  * a CIF geometry file compatible with gpawsolve's ``-g`` option
  * a Python configuration module that sets the key gpawsolve variables

Example
-------
python vaspconverter.py --poscar POSCAR --incar INCAR --kpoints KPOINTS --output-dir example_folder --system-name Silicon
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from ase.io import read, write


@dataclass
class IncarSettings:
    encut: Optional[float] = None
    ispin: Optional[int] = None
    sigma: Optional[float] = None
    ismear: Optional[int] = None
    magmoms: Optional[List[float]] = None
    nsw: Optional[int] = None
    ibrion: Optional[int] = None
    xc: Optional[str] = None
    ediff: Optional[float] = None


@dataclass
class KpointsSettings:
    mesh: Optional[List[int]] = None
    gamma_shift: bool = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert VASP input files into gpawsolve inputs.",
    )
    parser.add_argument("--poscar", required=True, type=Path, help="Path to POSCAR/CONTCAR file")
    parser.add_argument("--incar", type=Path, help="Path to INCAR file")
    parser.add_argument("--kpoints", type=Path, help="Path to KPOINTS file")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(), help="Directory to place generated files")
    parser.add_argument("--system-name", help="System name used for file stems and Outdirname")
    parser.add_argument("--input-filename", help="Optional override for the generated gpawsolve input filename")
    parser.add_argument("--outdirname", help="Override for Outdirname inside the generated gpawsolve input")
    parser.add_argument("--xc", help="Fallback XC functional if not specified in INCAR (default: PBE)")
    return parser.parse_args()


def parse_incar(path: Path, natoms: int) -> IncarSettings:
    raw: Dict[str, str] = {}
    for line in path.read_text().splitlines():
        clean = line.split("!")[0].split("#")[0].strip()
        if not clean or "=" not in clean:
            continue
        key, value = clean.split("=", 1)
        raw[key.strip().upper()] = value.strip()

    settings = IncarSettings()

    if "ENCUT" in raw:
        try:
            settings.encut = float(raw["ENCUT"].split()[0])
        except ValueError:
            pass

    if "ISPIN" in raw:
        try:
            settings.ispin = int(raw["ISPIN"].split()[0])
        except ValueError:
            pass

    if "SIGMA" in raw:
        try:
            settings.sigma = float(raw["SIGMA"].split()[0])
        except ValueError:
            pass

    if "ISMEAR" in raw:
        try:
            settings.ismear = int(raw["ISMEAR"].split()[0])
        except ValueError:
            pass

    if "MAGMOM" in raw:
        expanded = _expand_star_notation(raw["MAGMOM"]) or []
        if expanded:
            settings.magmoms = expanded[:natoms]

    if "NSW" in raw:
        try:
            settings.nsw = int(raw["NSW"].split()[0])
        except ValueError:
            pass

    if "IBRION" in raw:
        try:
            settings.ibrion = int(raw["IBRION"].split()[0])
        except ValueError:
            pass

    if "EDIFF" in raw:
        try:
            settings.ediff = float(raw["EDIFF"].split()[0])
        except ValueError:
            pass

    xc_candidates = (
        raw.get("GGA"),
        raw.get("METAGGA"),
        raw.get("LHFCALC"),
    )
    settings.xc = _map_xc_functional(xc_candidates)
    return settings


def parse_kpoints(path: Path) -> KpointsSettings:
    lines = [ln.strip().lower() for ln in path.read_text().splitlines() if ln.strip()]
    settings = KpointsSettings()
    if len(lines) < 3:
        return settings

    mode = lines[1]
    if mode.startswith("0") or mode.startswith("auto"):
        grid_line = 3 if len(lines) > 3 else 2
        if len(lines) > grid_line:
            settings.mesh = _parse_ints(lines[grid_line])
        if len(lines) > grid_line + 1:
            shift = lines[grid_line + 1].split()
            settings.gamma_shift = all(val in {"0", "0.0"} for val in shift)
    elif "gamma" in lines[2]:
        if len(lines) > 3:
            settings.mesh = _parse_ints(lines[3])
        settings.gamma_shift = True
    elif len(lines) >= 4 and any(tag in lines[2] for tag in ("monk", "gamma")):
        settings.mesh = _parse_ints(lines[3])
        settings.gamma_shift = "gamma" in lines[2]
    return settings


def _parse_ints(text: str) -> List[int]:
    ints: List[int] = []
    for token in text.replace(",", " ").split():
        try:
            ints.append(int(float(token)))
        except ValueError:
            continue
    return ints or [1, 1, 1]


def _expand_star_notation(expr: str) -> List[float]:
    values: List[float] = []
    for token in expr.replace(",", " ").split():
        if "*" in token:
            parts = token.split("*", 1)
            try:
                count = int(float(parts[0]))
                value = float(parts[1])
            except ValueError:
                continue
            values.extend([value] * count)
        else:
            try:
                values.append(float(token))
            except ValueError:
                continue
    return values


def _map_xc_functional(candidates: Iterable[Optional[str]]) -> Optional[str]:
    for candidate in candidates:
        if not candidate:
            continue
        token = candidate.strip().upper()
        if token in {"PE", "PBE"}:
            return "PBE"
        if token in {"PW91", "91"}:
            return "PW91"
        if token == "RP":
            return "RPBE"
        if token == "RE":
            return "revPBE"
        if token == "SCAN":
            return "SCAN"
        if token in {"T", "TPSS"}:
            return "TPSS"
        if token in {"HSE03", "HSE06"}:
            return token
        if token in {"B3LYP", "PBE0"}:
            return token
        if token in {"TRUE", "T"}:
            return "PBE0"
    return None


def determine_system_name(poscar_path: Path, explicit_name: Optional[str]) -> str:
    if explicit_name:
        return _sanitize_name(explicit_name)
    try:
        with poscar_path.open() as handle:
            title = handle.readline().strip()
            if title:
                return _sanitize_name(title)
    except OSError:
        pass
    return _sanitize_name(poscar_path.stem)


def _sanitize_name(name: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in name.strip())
    return safe or "system"


def build_config_lines(
    name: str,
    geom_filename: str,
    incar: IncarSettings,
    kpoints: KpointsSettings,
    args: argparse.Namespace,
    natoms: int,
) -> List[str]:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    outdirname = args.outdirname or f"{name}-results"
    xc = incar.xc or args.xc or "PBE"
    spin_calc = bool(incar.ispin == 2)
    magmom = None
    if spin_calc and incar.magmoms:
        magmom = sum(incar.magmoms[:natoms]) / min(len(incar.magmoms), natoms)

    lines = [
        f"# Auto-generated on {timestamp} by vaspconverter.py",
        f"Outdirname = '{outdirname}'",
        "",
        "Mode = 'PW'",
        "Ground_calc = True",
        f"Geo_optim = {bool(incar.ibrion and (incar.nsw or 0) > 0)}",
        "Elastic_calc = False",
        "DOS_calc = False",
        "Band_calc = False",
        "Density_calc = False",
        "Optical_calc = False",
        "",
        f"Cut_off_energy = {incar.encut if incar.encut else 340.0:.1f}",
    ]

    if kpoints.mesh:
        mesh = (kpoints.mesh + [1, 1, 1])[:3]
        lines.extend([
            f"Ground_kpts_x = {mesh[0]}",
            f"Ground_kpts_y = {mesh[1]}",
            f"Ground_kpts_z = {mesh[2]}",
        ])
        lines.append(f"Gamma = {kpoints.gamma_shift}")

    lines.extend([
        f"XC_calc = '{xc}'",
    ])

    if incar.sigma is not None:
        width = max(incar.sigma, 1e-3)
        lines.append(f"Occupation = {{'name': 'fermi-dirac', 'width': {width:.4f}}}")

    lines.append(f"Spin_calc = {spin_calc}")
    if magmom is not None:
        lines.append(f"Magmom_per_atom = {magmom:.4f}")

    if incar.ediff is not None:
        lines.append(f"Ground_convergence = {{'energy': {incar.ediff}}}")

    lines.extend([
        "MPI_cores = 4",
        "Localisation = 'en_UK'",
        "",
        f"# Geometry file to use with gpawsolve.py: {geom_filename}",
    ])

    return [line.rstrip() for line in lines]


def main() -> None:
    args = parse_args()
    poscar_path = args.poscar.resolve()
    if not poscar_path.exists():
        raise FileNotFoundError(f"POSCAR file not found: {poscar_path}")

    structure = read(poscar_path)
    natoms = len(structure)

    name = determine_system_name(poscar_path, args.system_name)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    geom_filename = f"{name}.cif"
    geometry_path = output_dir / geom_filename
    write(geometry_path, structure, format='cif')

    incar_settings = IncarSettings()
    if args.incar:
        incar_path = args.incar.resolve()
        if not incar_path.exists():
            raise FileNotFoundError(f"INCAR file not found: {incar_path}")
        incar_settings = parse_incar(incar_path, natoms)

    kpoints_settings = KpointsSettings()
    if args.kpoints:
        kpoints_path = args.kpoints.resolve()
        if not kpoints_path.exists():
            raise FileNotFoundError(f"KPOINTS file not found: {kpoints_path}")
        kpoints_settings = parse_kpoints(kpoints_path)

    input_filename = args.input_filename or f"{name}.py"
    input_path = output_dir / input_filename
    config_lines = build_config_lines(
        name=name,
        geom_filename=geom_filename,
        incar=incar_settings,
        kpoints=kpoints_settings,
        args=args,
        natoms=natoms,
    )
    input_path.write_text("\n".join(config_lines) + "\n")

    print(f"Wrote geometry to {geometry_path}")
    print(f"Wrote gpawsolve input to {input_path}")
    print(f"Run: gpawsolve.py -i {input_path} -g {geometry_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
