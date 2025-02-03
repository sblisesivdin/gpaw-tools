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

import sys
import os
import time
import spglib as spg
import textwrap
import requests
from argparse import ArgumentParser, HelpFormatter
from pathlib import Path
from ase import *
from ase.io import read
from ase.io.cif import write_cif
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
__version__ = "v25.2.2b1"

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
args = None

args = parser.parse_args()

if args is None:
    print(" Please enter input file (-i) and geometry file (-g) to execute.")
    exit(0)

outdir = True
inFile = None
Outdirname = ''

try:
    if args.inputfile is not None:
        configpath = os.path.join(os.getcwd(),args.inputfile)
        sys.path.append(os.getcwd())
        # Works like from FILE import *
        conf = __import__(Path(configpath).stem, globals(), locals(), ['*'])
        for k in dir(conf):
            locals()[k] = getattr(conf, k)

    if args.geometryfile :
        inFile = os.path.join(os.getcwd(),args.geometryfile)
    
    if args.version == True:
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
        except (requests.ConnectionError, requests.Timeout) as exception:
            print('-------------------------------------------------------------------------------------------------------')
            print('gpaw-tools: This is asapsolve.py uses ASAP3 '+asap3.__version__+', ASE '+ase.__version__)
            print('-------------------------------------------------------------------------------------------------------')
            print('No internet connection available.')
        quit()      

except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

# If there is a CIF input, use it. Otherwise use the bulk configuration provided above.
if inFile is None:
    if Outdirname !='':
        struct = Outdirname
    else:
        struct = 'results' # All files will get their names from this file
    print("Number of atoms provided in Atoms object:"+str(bulk_configuration.get_global_number_of_atoms()))
else:
    struct = Path(inFile).stem
    bulk_configuration = read(inFile, index='-1')
    print("Number of atoms imported from CIF file:"+str(bulk_configuration.get_global_number_of_atoms()))
    print("Spacegroup of CIF file (SPGlib):",spg.get_spacegroup(bulk_configuration))

# Control outdir
if Outdirname != '':
    structpath = os.path.join(os.getcwd(),Outdirname)
else:
    structpath = os.path.join(os.getcwd(),struct)

if not os.path.isdir(structpath):
    os.makedirs(structpath, exist_ok=True)
struct = os.path.join(structpath,struct)

asestruct = bulk_configuration

asestruct.set_calculator(KIM(OpenKIM_potential, options={"ase_neigh": False}))

dyn = Langevin(asestruct, timestep=Time*units.fs, trajectory=struct+'-Results.traj', logfile=struct+'-Log.txt', temperature_K=Temperature, friction=Friction)

print("")
print("Energy per atom:")
print("  %15s %15s %15s" % ("Pot. energy", "Kin. energy", "Total energy"))

for _ in range(25):
    dyn.run(10)
    epot = asestruct.get_potential_energy()/len(asestruct)
    ekin = asestruct.get_kinetic_energy()/len(asestruct)
    print("%15.5f %15.5f %15.5f" % (epot, ekin, epot+ekin))

# PRINT TO FILE PART -----------------------------------
with open(struct+'Results.py', 'w') as f:
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


def print_attention_message():
    print("    )")
    print("ATTENTION: If you have double number of atoms, it may be caused by ")
    print("           repeating ASE bug https://gitlab.com/ase/ase/-/issues/169 ")
    print("           Please assign Solve_double_element_problem variable as True in this script if necessary.")

def export_cif(asestruct, bulk_configuration):
    write_cif(struct+'-FinalStructure.cif', bulk_configuration)

print_attention_message()
export_cif(struct, bulk_configuration)
