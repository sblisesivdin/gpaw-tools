#!/usr/bin/env python

'''
asapsolve.py: Quick Geometric Optimization
              using interatomic potentials.
More information: $ asapsolve.py -h
'''

Description = f''' 
 Usage: 
 $ asapsolve.py <args>
 
 -------------------------------------------------------------
   Some potentials
 -------------------------------------------------------------
 | Name                                                  | Information                           | 
 | ----------------------------------------------------- | ------------------------------------- |
 | LJ_ElliottAkerson_2015_Universal__MO_959249795837_003 | General potential for all elements    |
 
 '''

import getopt
import sys
import os
import time
import textwrap
import requests
from argparse import ArgumentParser, HelpFormatter
from pathlib import Path
from numbers import Number
from itertools import product
from ase import *
from ase.io import read
from ase.io.cif import write_cif
from ase.spacegroup import get_spacegroup
from asap3 import Atoms, units
from asap3.md.langevin import Langevin
from ase.calculators.kim import KIM


# -------------------------------------------------------------
# Parameters
# -------------------------------------------------------------

# Simulation parameters
OpenKIM_potential = 'LJ_ElliottAkerson_2015_Universal__MO_959249795837_003'
Temperature = 1 # Kelvin
Time = 5 # fs
Friction = 0.05

# Molecular dynamics loop configuration
MD_cycles = 25
MD_steps_per_cycle = 10

# Short aliases for verbose OpenKIM potential identifiers
POTENTIAL_ALIASES = {
    'lj': 'LJ_ElliottAkerson_2015_Universal__MO_959249795837_003',
}


def _ensure_iterable(value):
    """Normalize schedule-like inputs into a list of floats."""
    if isinstance(value, tuple):
        if len(value) == 3 and all(isinstance(i, Number) for i in value):
            start, stop, step = value
            if step == 0:
                raise ValueError('Step cannot be zero when defining a range.')
            seq = []
            current = start
            comparison = (lambda a, b: a <= b + 1e-12) if step > 0 else (lambda a, b: a >= b - 1e-12)
            while comparison(current, stop):
                seq.append(current)
                current += step
            return seq
        return list(value)
    if isinstance(value, list):
        return list(value)
    if isinstance(value, dict):
        start = value.get('start')
        stop = value.get('stop', start)
        count = value.get('count')
        step = value.get('step')
        if start is None:
            raise ValueError('Range dictionaries must define a "start" key.')
        if count:
            if count <= 1:
                return [float(start)]
            delta = (stop - start) / (count - 1)
            return [start + delta * idx for idx in range(count)]
        if step is None:
            return [float(start), float(stop)] if stop is not None else [float(start)]
        if step == 0:
            raise ValueError('Step cannot be zero when defining a range.')
        seq = []
        current = start
        comparison = (lambda a, b: a <= b + 1e-12) if step > 0 else (lambda a, b: a >= b - 1e-12)
        while comparison(current, stop):
            seq.append(current)
            current += step
        return seq
    if isinstance(value, Number):
        return [value]
    return []


def _build_profile(name, base_value, cycle_count, namespace):
    """Return per-cycle parameter profile with graceful fallbacks."""
    keys = [f"{name}_profile", f"{name}_range"]
    sequence = []
    for key in keys:
        if key in namespace:
            sequence = _ensure_iterable(namespace[key])
            break
    if not sequence:
        sequence = _ensure_iterable(namespace.get(name, base_value))
    if not sequence:
        sequence = [base_value]
    if len(sequence) >= cycle_count:
        return sequence[:cycle_count]
    return sequence + [sequence[-1]] * (cycle_count - len(sequence))


def _resolve_potential(namespace, alias):
    """Resolve OpenKIM potential either from alias or explicit id."""
    if alias and alias in POTENTIAL_ALIASES:
        return POTENTIAL_ALIASES[alias]
    if alias and alias not in POTENTIAL_ALIASES:
        raise KeyError(f'Unknown potential alias: {alias}')
    potential = namespace.get('OpenKIM_potential', OpenKIM_potential)
    alias_key = namespace.get('OpenKIM_potential_alias')
    if alias_key:
        if alias_key in POTENTIAL_ALIASES:
            potential = POTENTIAL_ALIASES[alias_key]
        else:
            raise KeyError(f'Unknown potential alias: {alias_key}')
    return potential


def _write_energy_csv(path, records):
    if not records:
        return
    header = "Step,Cycle,PotentialEnergyPerAtom(eV),KineticEnergyPerAtom(eV),TotalEnergyPerAtom(eV),Temperature(K),TimeStep(fs),Friction"
    with open(path, 'w') as fd:
        fd.write(header + "\n")
        for rec in records:
            fd.write(
                f"{rec['step']},{rec['cycle']},{rec['epot']:.6f},{rec['ekin']:.6f},{rec['total']:.6f},{rec['temperature']:.6f},{rec['timestep']:.6f},{rec['friction']:.6f}\n"
            )


def _get_run_values(name, default, namespace):
    values_key = f"{name}_values"
    if values_key in namespace:
        seq = _ensure_iterable(namespace[values_key])
        if seq:
            return seq
    value = namespace.get(name, default)
    if isinstance(value, Number):
        return [value]
    seq = _ensure_iterable(value)
    return seq if seq else [default]


def _format_suffix(prefix, value):
    if isinstance(value, Number):
        formatted = ('{:.6g}'.format(value)).replace('-', 'm').replace('.', 'p')
    else:
        formatted = str(value)
    return f"{prefix}{formatted}"


def _print_attention_message():
    print("    )")
    print("ATTENTION: If you have double number of atoms, it may be caused by ")
    print("           repeating ASE bug https://gitlab.com/ase/ase/-/issues/169 ")
    print("           Please assign Solve_double_element_problem variable as True in this script if necessary.")


def _export_cif(struct_prefix, atoms):
    write_cif(struct_prefix+'-FinalStructure.cif', atoms)


Scaled = False # Scaled or Cartesian coordinates
Manual_PBC = False # If you need manual constraint axis

# If Manual_PBC is true then change following:
PBC_constraints = [True, True, False]

# If you have double number of elements in your final file
Solve_double_element_problem = True

# If you do not want to use a CIF file for geometry, please provide
# ASE Atoms object information below. You can use ciftoase.py to
# make your own ASE Atoms object from a CIF file.
# -------------------------------------------------------------
# Bulk Configuration
# -------------------------------------------------------------

bulk_configuration = Atoms(
    [
        Atom('Ge', (1.222474e-31, 4.094533468076675e-32, 5.02)),
        Atom('Ge', (-1.9999999993913775e-06, 2.3094022314590417, 4.98)),
    ],
    cell=[
        (4.0, 0.0, 0.0),
        (-1.9999999999999991, 3.464101615137755, 0.0),
        (0.0, 0.0, 20.0)
    ],
    pbc=True,
)
# -------------------------------------------------------------
# ///////   YOU DO NOT NEED TO CHANGE ANYTHING BELOW    \\\\\\\
# -------------------------------------------------------------
# Version
__version__ = "v25.10.1b1"

# Start time
time0 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
# To print Description variable with argparse
class RawFormatter(HelpFormatter):
    def _fill_text(self, text, width, indent):
        return "\n".join([textwrap.fill(line, width) for line in textwrap.indent(textwrap.dedent(text), indent).splitlines()])

# Arguments parsing
parser = ArgumentParser(prog ='asapsolve.py', description=Description, formatter_class=RawFormatter)


parser.add_argument("-i", "--input", dest = "inputfile", help="Use input file for calculation variables (also you can insert geometry)")
parser.add_argument("-g", "--geometry",dest ="geometryfile", help="Use CIF file for geometry")
parser.add_argument("-v", "--version", dest="version", action='store_true')

args = parser.parse_args()

if args.version:
    import asap3
    import ase
    try:
        response = requests.get("https://api.github.com/repos/sblisesivdin/gpaw-tools/releases/latest", timeout=5)
        print('-------------------------------------------------------------------------------------------------------')
        print('\033[95mgpaw-tools:\033[0m This is asapsolve.py uses ASAP3 '+asap3.__version__+', and ASE '+ase.__version__)
        print('-------------------------------------------------------------------------------------------------------')
        print('The latest STABLE release was '+response.json()["tag_name"]+', which is published at '+response.json()["published_at"])
        print('Download the latest STABLE tarball release at: '+response.json()["tarball_url"])
        print('Download the latest STABLE zipball release at: '+response.json()["zipball_url"])
        print('Download the latest DEV zipball release at: https://github.com/lrgresearch/gpaw-tools/archive/refs/heads/main.zip')
    except (requests.ConnectionError, requests.Timeout):
        print('-------------------------------------------------------------------------------------------------------')
        print('gpaw-tools: This is asapsolve.py uses ASAP3 '+asap3.__version__+', ASE '+ase.__version__)
        print('-------------------------------------------------------------------------------------------------------')
        print('No internet connection available.')
    sys.exit(0)

if not args.inputfile or not args.geometryfile:
    print('ERROR: Please provide both input (-i) and geometry (-g) files.')
    sys.exit(1)

Outdirname = ''
configpath = None
config_dir = Path.cwd()
input_stem = None
inFile = None

try:
    configpath = Path(args.inputfile).expanduser()
    if not configpath.is_absolute():
        configpath = (Path.cwd() / configpath).resolve()
    config_dir = configpath.parent
    input_stem = configpath.stem
    if str(config_dir) not in sys.path:
        sys.path.append(str(config_dir))
    conf = __import__(configpath.stem, globals(), locals(), ['*'])
    for k in dir(conf):
        globals()[k] = getattr(conf, k)

    geometry_path = Path(args.geometryfile).expanduser()
    if not geometry_path.is_absolute():
        geometry_path = (config_dir / geometry_path).resolve()
    inFile = str(geometry_path)

except getopt.error as err:
    print(str(err))

namespace = globals()

try:
    resolved_potential = _resolve_potential(namespace, None)
except KeyError as exc:
    print(str(exc))
    sys.exit(1)

OpenKIM_potential = resolved_potential
namespace['OpenKIM_potential'] = OpenKIM_potential

if MD_cycles <= 0:
    print('MD_cycles must be a positive integer.')
    sys.exit(1)

if MD_steps_per_cycle <= 0:
    print('MD_steps_per_cycle must be a positive integer.')
    sys.exit(1)

# Geometry input is mandatory
if inFile is None:
    print('ERROR: Geometry file could not be resolved.')
    sys.exit(1)

struct_name = Path(inFile).stem
bulk_configuration = read(inFile, index='-1')
print("Number of atoms imported from CIF file:"+str(bulk_configuration.get_global_number_of_atoms()))
try:
    spacegroup = get_spacegroup(bulk_configuration, symprec=1e-2)
    print("Spacegroup of CIF file (ASE):", f"{spacegroup.symbol} (No. {spacegroup.no})")
except Exception as exc:
    print(f"Could not determine spacegroup: {exc}")

base_directory = config_dir if configpath else Path.cwd()

if Outdirname != '':
    structpath = Path(Outdirname)
    if not structpath.is_absolute():
        structpath = (base_directory / structpath).resolve()
else:
    if inFile is not None:
        structdir = Path(inFile).resolve().parent
        structpath = (structdir / f"{struct_name}_results").resolve()
    elif input_stem is not None:
        structpath = (config_dir / input_stem).resolve()
    else:
        structpath = (base_directory / struct_name).resolve()

if not os.path.isdir(structpath):
    os.makedirs(structpath, exist_ok=True)

if inFile is not None:
    struct_base = os.path.join(str(structpath), struct_name)
elif input_stem is not None:
    struct_base = os.path.join(str(structpath), input_stem)
else:
    struct_base = os.path.join(str(structpath), struct_name)

initial_structure = bulk_configuration.copy()
temperature_options = [float(v) for v in _get_run_values('Temperature', Temperature, namespace)]
time_options = [float(v) for v in _get_run_values('Time', Time, namespace)]
friction_options = [float(v) for v in _get_run_values('Friction', Friction, namespace)]

combinations = list(product(temperature_options, time_options, friction_options))
varying_lengths = {
    'T': len(set(temperature_options)),
    'dt': len(set(time_options)),
    'fr': len(set(friction_options))
}

original_temperature = namespace.get('Temperature', Temperature)
original_time = namespace.get('Time', Time)
original_friction = namespace.get('Friction', Friction)

for combo_index, (temperature_value, timestep_value, friction_value) in enumerate(combinations, 1):
    asestruct = initial_structure.copy()
    asestruct.set_calculator(KIM(OpenKIM_potential, options={"ase_neigh": False}))

    suffix_parts = []
    if len(combinations) > 1:
        if varying_lengths['T'] > 1:
            suffix_parts.append(_format_suffix('T', temperature_value))
        if varying_lengths['dt'] > 1:
            suffix_parts.append(_format_suffix('dt', timestep_value))
        if varying_lengths['fr'] > 1:
            suffix_parts.append(_format_suffix('fr', friction_value))
    run_struct = struct_base if not suffix_parts else struct_base + '_' + '_'.join(suffix_parts)
    struct_prefix = run_struct

    namespace['Temperature'] = temperature_value
    namespace['Time'] = timestep_value
    namespace['Friction'] = friction_value

    temperature_profile = _build_profile('Temperature', temperature_value, MD_cycles, namespace)
    time_profile = _build_profile('Time', timestep_value, MD_cycles, namespace)
    friction_profile = _build_profile('Friction', friction_value, MD_cycles, namespace)

    initial_temperature = float(temperature_profile[0])
    initial_timestep = float(time_profile[0])
    initial_friction = float(friction_profile[0])

    dyn = Langevin(
        asestruct,
        timestep=initial_timestep*units.fs,
        trajectory=struct_prefix+'-Results.traj',
        logfile=struct_prefix+'-Log.txt',
        temperature_K=initial_temperature,
        friction=initial_friction
    )

    if len(combinations) > 1:
        print("")
        print(f"Run {combo_index}/{len(combinations)}: T={temperature_value} K, dt={timestep_value} fs, friction={friction_value}")

    print("")
    print("Energy per atom (cycle averages):")
    print("  %6s %15s %15s %15s %12s %12s %12s" % ("Cycle", "Pot. energy", "Kin. energy", "Total energy", "Temp (K)", "dt (fs)", "Friction"))

    energy_records = []
    total_steps = 0

    for cycle in range(MD_cycles):
        current_temperature = float(temperature_profile[cycle])
        current_timestep = float(time_profile[cycle])
        current_friction = float(friction_profile[cycle])

        if cycle > 0:
            if abs(current_temperature - initial_temperature) > 1e-9:
                dyn.set_temperature(current_temperature)
            if abs(current_timestep - initial_timestep) > 1e-12:
                dyn.set_timestep(current_timestep*units.fs)
            if abs(current_friction - initial_friction) > 1e-12:
                dyn.set_friction(current_friction)

        dyn.run(MD_steps_per_cycle)
        total_steps += MD_steps_per_cycle
        epot = asestruct.get_potential_energy()/len(asestruct)
        ekin = asestruct.get_kinetic_energy()/len(asestruct)
        total_energy = epot + ekin
        print("%7d %15.5f %15.5f %15.5f %12.2f %12.3f %12.5f" % (cycle+1, epot, ekin, total_energy, current_temperature, current_timestep, current_friction))
        energy_records.append({
            'cycle': cycle + 1,
            'step': total_steps,
            'epot': epot,
            'ekin': ekin,
            'total': total_energy,
            'temperature': current_temperature,
            'timestep': current_timestep,
            'friction': current_friction
        })

        initial_temperature = current_temperature
        initial_timestep = current_timestep
        initial_friction = current_friction

    # PRINT TO FILE PART -----------------------------------
    _write_energy_csv(struct_prefix+'-Energy.csv', energy_records)

    with open(struct_prefix+'Results.py', 'w') as f:
        f.write("bulk_configuration = Atoms(\n")
        f.write("    [\n")
        if Scaled == True:
            positions = asestruct.get_scaled_positions()
        else:
            positions = asestruct.get_positions()
        nn=0
        mm=0

        if Solve_double_element_problem == True:
            for n in asestruct.get_chemical_symbols():
                nn=nn+1
                for m in positions:
                    mm=mm+1
                    if mm == nn:
                        f.write("    Atom('"+n+"', ( "+str(m[0])+", "+str(m[1])+", "+str(m[2])+" )),\n")
                mm=0
        else:
            for n in asestruct.get_chemical_symbols():
                for m in positions:
                    f.write("    Atom('"+n+"', ( "+str(m[0])+", "+str(m[1])+", "+str(m[2])+" )),\n")
        f.write("    ],\n")
        f.write("    cell=[("+str(asestruct.cell[0,0])+", "+str(asestruct.cell[0,1])+", "+str(asestruct.cell[0,2])+"), ("+str(asestruct.cell[1,0])+", "+str(asestruct.cell[1,1])+", "+str(asestruct.cell[1,2])+"), ("+str(asestruct.cell[2,0])+", "+str(asestruct.cell[2,1])+", "+str(asestruct.cell[2,2])+")],\n")
        if Manual_PBC == False:
            f.write("    pbc=True,\n")
        else:
            f.write("    pbc=["+str(PBC_constraints[0])+","+str(PBC_constraints[1])+","+str(PBC_constraints[2])+"],\n")
        f.write("    )\n")

    _print_attention_message()
    _export_cif(struct_prefix, asestruct)

namespace['Temperature'] = original_temperature
namespace['Time'] = original_time
namespace['Friction'] = original_friction
