#!/usr/bin/env python3
"""Convert a Quantum ESPRESSO pw.x input into gpawsolve-ready files.

The script reads a pw.x style input file, extracts common calculation
parameters and lattice/atomic structure, then produces:
  * a CIF geometry file for use with gpawsolve's ``-g`` option.
  * a Python configuration module defining the gpawsolve variables.

Example
-------
python converters/qeconverter.py --input si.scf.in --output-dir example_folder --system-name SiliconQE
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from ase.io import read, write

RY_TO_EV = 13.605693009


@dataclass
class QEInputSettings:
    calculation: Optional[str] = None
    ecutwfc: Optional[float] = None
    occupations: Optional[str] = None
    smearing: Optional[str] = None
    degauss: Optional[float] = None
    nspin: Optional[int] = None
    starting_magnetization: Dict[str, float] = field(default_factory=dict)
    conv_thr: Optional[float] = None
    k_mesh: Optional[List[int]] = None
    k_shift: Optional[List[int]] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Quantum ESPRESSO pw.x input into gpawsolve inputs.",
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to pw.x input file")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(), help="Directory for generated files")
    parser.add_argument("--system-name", help="System name used for file stems and Outdirname")
    parser.add_argument("--outdirname", help="Override Outdirname value inside the generated input")
    parser.add_argument("--input-filename", help="Override gpawsolve input filename")
    parser.add_argument("--xc", help="Optional XC functional override (default PBE)")
    return parser.parse_args()


def clean_line(line: str) -> str:
    return line.split("!")[0].split("#")[0].strip()


def parse_qe_input(path: Path) -> QEInputSettings:
    settings = QEInputSettings()
    lines = [clean_line(ln) for ln in path.read_text().splitlines()]
    lines = [ln for ln in lines if ln]

    current_section = None
    expect_kpoints = False
    k_mode: Optional[str] = None

    for line in lines:
        upper = line.upper()
        if upper.startswith("&"):
            current_section = upper[1:]
            continue
        if upper == "/":
            current_section = None
            continue

        if upper.startswith("K_POINTS"):
            parts = line.split()
            k_mode = parts[1].lower() if len(parts) > 1 else "automatic"
            expect_kpoints = True
            continue

        if expect_kpoints:
            expect_kpoints = False
            tokens = line.split()
            if k_mode.startswith("auto"):
                mesh = [int(float(token)) for token in tokens[:3]]
                shift = [int(float(token)) for token in tokens[3:6]] if len(tokens) >= 6 else [0, 0, 0]
                settings.k_mesh = mesh
                settings.k_shift = shift
            elif k_mode.startswith("gamma"):
                settings.k_mesh = [1, 1, 1]
                settings.k_shift = [0, 0, 0]
            else:
                nums = [int(float(token)) for token in tokens[:3]] if len(tokens) >= 3 else [1, 1, 1]
                settings.k_mesh = nums
                settings.k_shift = [0, 0, 0]
            continue

        if "=" in line:
            key, value = [part.strip() for part in line.split("=", 1)]
            key_lower = key.lower()

            if key_lower.startswith("starting_magnetization"):
                species_match = re.search(r"starting_magnetization\(([^)]+)\)", key_lower)
                species = species_match.group(1) if species_match else "default"
                try:
                    settings.starting_magnetization[species] = float(value.rstrip(',').replace('d', 'e'))
                except ValueError:
                    pass
                continue

            value_clean = value.rstrip(",").replace("'", "").replace('"', '').strip()
            value_clean = value_clean.replace(".true.", "True").replace(".false.", "False")
            value_clean = value_clean.replace('d', 'e')

            if key_lower == "calculation":
                settings.calculation = value_clean.lower()
            elif key_lower == "ecutwfc":
                try:
                    settings.ecutwfc = float(value_clean)
                except ValueError:
                    pass
            elif key_lower == "occupations":
                settings.occupations = value_clean.lower()
            elif key_lower == "smearing":
                settings.smearing = value_clean.lower()
            elif key_lower == "degauss":
                try:
                    settings.degauss = float(value_clean)
                except ValueError:
                    pass
            elif key_lower == "nspin":
                try:
                    settings.nspin = int(float(value_clean))
                except ValueError:
                    pass
            elif key_lower == "conv_thr":
                try:
                    settings.conv_thr = float(value_clean)
                except ValueError:
                    pass
    return settings


def determine_system_name(input_path: Path, override: Optional[str]) -> str:
    if override:
        return _sanitize_name(override)
    return _sanitize_name(input_path.stem)


def _sanitize_name(name: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in name.strip())
    return safe or "system"


def build_config_lines(
    name: str,
    geom_filename: str,
    settings: QEInputSettings,
    args: argparse.Namespace,
) -> List[str]:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    outdirname = args.outdirname or f"{name}-results"
    xc = args.xc or "PBE"
    spin_calc = settings.nspin == 2

    lines: List[str] = [
        f"# Auto-generated on {timestamp} by qeconverter.py",
        f"Outdirname = '{outdirname}'",
        "",
        "Mode = 'PW'",
        "Ground_calc = True",
        f"Geo_optim = {settings.calculation in {'relax', 'vc-relax'}}",
        "Elastic_calc = False",
        "DOS_calc = False",
        "Band_calc = False",
        "Density_calc = False",
        "Optical_calc = False",
        "",
    ]

    if settings.ecutwfc is not None:
        lines.append(f"Cut_off_energy = {settings.ecutwfc * RY_TO_EV:.1f}")
    else:
        lines.append("Cut_off_energy = 340.0")

    if settings.k_mesh:
        mesh = settings.k_mesh + [1, 1, 1]
        mesh = mesh[:3]
        lines.extend([
            f"Ground_kpts_x = {mesh[0]}",
            f"Ground_kpts_y = {mesh[1]}",
            f"Ground_kpts_z = {mesh[2]}",
        ])
        if settings.k_shift:
            gamma = all(shift == 0 for shift in settings.k_shift[:3])
            lines.append(f"Gamma = {gamma}")

    lines.append(f"XC_calc = '{xc}'")

    if settings.occupations in {"smearing", "tetrahedra", "tetrahedra_opt"} and settings.degauss:
        width = max(settings.degauss * RY_TO_EV, 1e-3)
        lines.append(f"Occupation = {{'name': 'fermi-dirac', 'width': {width:.4f}}}")

    lines.append(f"Spin_calc = {spin_calc}")

    if settings.conv_thr is not None:
        energy_conv = settings.conv_thr * RY_TO_EV
        lines.append(f"Ground_convergence = {{'energy': {energy_conv}}}")

    lines.extend([
        "MPI_cores = 4",
        "Localisation = 'en_UK'",
        "",
        f"# Geometry file to use with gpawsolve.py: {geom_filename}",
    ])

    return [line.rstrip() for line in lines]


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Quantum ESPRESSO input not found: {input_path}")

    atoms = read(input_path, format='espresso-in')
    name = determine_system_name(input_path, args.system_name)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    geom_filename = f"{name}.cif"
    geometry_path = output_dir / geom_filename
    write(geometry_path, atoms, format='cif')

    settings = parse_qe_input(input_path)

    input_filename = args.input_filename or f"{name}.py"
    input_path_out = output_dir / input_filename
    config_lines = build_config_lines(
        name=name,
        geom_filename=geom_filename,
        settings=settings,
        args=args,
    )
    input_path_out.write_text("\n".join(config_lines) + "\n")

    print(f"Wrote geometry to {geometry_path}")
    print(f"Wrote gpawsolve input to {input_path_out}")
    print(f"Run: gpawsolve.py -i {input_path_out} -g {geometry_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
