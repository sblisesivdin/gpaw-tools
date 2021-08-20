from ase import *
from ase.parallel import paropen, world, parprint
from gpaw import GPAW
from ase.optimize.lbfgs import LBFGS
from ase.io import read, write
import matplotlib.pyplot as plt
from ase.dft.dos import DOS
from gpaw.utilities.dos import RestartLCAODOS, fold
#from ase.constraints import UnitCellFilter
from pathlib import Path
from ase.units import Hartree

# Sample Electronic Calculation GPAW Input for LRG Studies
# by Sefer Bora Lisesivdin
# August 2021 - BFGS to LBFGS, Small many changes 
# July 2021 - Corrected version
# March 2020 - First Version 
# Usage: Change number with core numbers/threads to use. I am suggesting to use total number of cores(or threads) - 1
# Usage: $ gpaw -P8 python GPAWSimpleBenchmark2021.py
# For AMD CPUs or using Intel CPUs without hyperthreading: (Example CPU is intel here, 4 cores or 8 threads)
#        $ mpirun -n 4 gpaw python GPAWSimpleBenchmark2021.py
# For using all threads provided by Intel Hyperthreading technology:
#        $ mpirun --use-hwthread-cpus -n 8 gpaw python GPAWSimpleBenchmark2021.py 
# -------------------------------------------------------------
# Parameters
# -------------------------------------------------------------
fmaxval = 0.05 			#
cut_off_energy = 340 	# eV
kpts_x = 5 			# kpoints in x direction
kpts_y = 5				# kpoints in y direction
kpts_z = 1				# kpoints in z direction
band_path = 'GMKG'	# Brillouin zone high symmetry points
band_npoints = 40		# Number of points between high symmetry points 
energy_max = 15         # eV. It is the maximum energy value for band structure figure.
NumberOfAtomicOrb = 104 # Number of atomic orbitals.	    	
#Exchange-Correlation, choose one:
#XC_calc = 'LDA'
XC_calc = 'PBE'
#XC_calc = 'revPBE'
#XC_calc = 'RPBE'

draw_graphs = "yes"			# Draw DOS and band structure on screen (yes for draw, small letters)
# Which components of strain will be relaxed
# EpsX, EpsY, EpsZ, ShearYZ, ShearXZ, ShearXY
# Example: For a x-y 2D nanosheet only first 2 component will be true
whichstrain=[False, False, False, False, False, False]

WantCIFexport = False
# -------------------------------------------------------------
# Bulk Configuration
# -------------------------------------------------------------
bulk_configuration = Atoms(
    [
    Atom('C', ( 0.0, 0.0, 5.0 )),
    Atom('C', ( -1.2339999999999995, 2.1373506965399947, 5.0 )),
    Atom('C', ( 2.4679999999999995, 0.0, 5.0 )),
    Atom('C', ( 1.234, 2.1373506965399947, 5.0 )),
    Atom('C', ( 2.468000000230841e-06, 1.424899039459532, 5.0 )),
    Atom('C', ( -1.2339975319999992, 3.5622497359995267, 5.0 )),
    Atom('C', ( 2.4680024680000003, 1.424899039459532, 5.0 )),
    Atom('C', ( 1.234002468000001, 3.5622497359995267, 5.0 )),
    ],
    cell=[(4.936, 0.0, 0.0), (-2.467999999999999, 4.274701393079989, 0.0), (0.0, 0.0, 20.0)],
    pbc=True,
    )

# -------------------------------------------------------------
# ///////   YOU DO NOT NEED TO CHANGE ANYTHING BELOW    \\\\\\\ 
# -------------------------------------------------------------
struct = Path(__file__).stem # All files will get their names from this file
# -------------------------------------------------------------
# Step 1 - GROUND STATE
# -------------------------------------------------------------
calc = GPAW(mode='lcao', basis='dzp', kpts=(5, 5, 1), parallel={'domain': world.size})
bulk_configuration.calc = calc

#uf = UnitCellFilter(bulk_configuration, mask=whichstrain)
#relax = LBFGS(uf, trajectory=struct+'-1-Result-Ground.traj')
relax = LBFGS(bulk_configuration, trajectory=struct+'-1-Result-Ground.traj')
relax.run(fmax=fmaxval)  # Consider much tighter fmax!

bulk_configuration.get_potential_energy()
calc.write(struct+'-1-Result-Ground.gpw')

# -------------------------------------------------------------
# Step 2 - DOS CALCULATION
# -------------------------------------------------------------
calc = GPAW(struct+'-1-Result-Ground.gpw', txt=struct+'-2-Log-DOS.txt')
#energies, weights = calc.get_dos(npts=800, width=0)
dos = RestartLCAODOS(calc)
energies, weights = dos.get_subspace_pdos(range(NumberOfAtomicOrb))
ef = calc.get_fermi_level()
e, w = fold(energies * Hartree, weights, 2000, 0.1)
fd = open(struct+'-2-Result-DOS.txt', "w")
for x in zip(e-ef, w):
    print(*x, sep=", ", file=fd)
fd.close()

if draw_graphs == "yes":
    if world.rank == 0:
	# Draw graphs only on master node
        ax = plt.gca()
        ax.plot(e-ef, w)
        ax.set_xlabel('Energy [eV]')
        ax.set_ylabel('DOS [1/eV]')
        plt.savefig(struct+'-2-Graph-DOS.png')
        #plt.show()

# -------------------------------------------------------------
# Step 3 - BAND STRUCTURE CALCULATION
# -------------------------------------------------------------
calc = GPAW(struct+'-1-Result-Ground.gpw',
	    txt=struct+'-3-Log-Band.txt',
	    fixdensity=True,
	    symmetry='off',
	    kpts={'path': band_path, 'npoints': band_npoints},
	    convergence={'bands': 16})

calc.get_potential_energy()
bs = calc.band_structure()
ef = calc.get_fermi_level()
num_of_bands = calc.get_number_of_bands()
parprint('Num of bands:'+str(num_of_bands))

#bs.write(struct+'-3-Result-Band.json')
calc.write(struct+'-3-Result-Band.gpw')
if draw_graphs == "yes":
    if world.rank == 0:
	# Draw graphs only on master node
        bs.plot(filename=struct+'-3-Graph-Band.png', show=True, emax=energy_max)

# Extract eigenenergies into a file for plotting with some external package

import numpy as np
calc = GPAW(struct+'-3-Result-Band.gpw', txt=None)
eps_skn = np.array([[calc.get_eigenvalues(k,s)
                     for k in range(band_npoints)]
                    for s in range(1)]) - ef

f = open(struct+'-3-Result-Band.dat', 'w')
for n in range(num_of_bands):
    for k in range(band_npoints):
        print(k, eps_skn[0, k, n], end="\n", file=f)
    print (end="\n", file=f)
f.close()


# - - - - - - - - - COLUMNED OUTPUT - - - - - - - - - - 
# create a  matrix of zeroes
arr = [[0 for col in range(2*num_of_bands+1)] for row in range(band_npoints+1)]
f = open(struct+'-3-Result-Band.dat', 'r')
lines = f.readlines()
f.close()
a = 0 

for i in range(0, num_of_bands, 1):
   b = 0
   for a in range (a, a+band_npoints, 1):
      fields = lines[a].split()
      arr[b][2*i] = fields[0]
      arr[b][2*i+1] = fields[1]
      b = b + 1
   a = a + 2

# writing to output file
f = open(struct+'-3-Result-Band-withColumns.dat', 'w')
stringline = ""

for i in range(0, band_npoints, 1):
    stringline = stringline + arr[i][0] + " " + arr[i][1] + " "
    for j in range(1, num_of_bands, 1):
        stringline = stringline + arr[i][2*j+1] + " "
    f.write(stringline + "\n")
    stringline = ""

f.close()

# -------------------------------------------------------------
# Step 4 - BAND STRUCTURE CIF EXPORT
# -------------------------------------------------------------
if WantCIFexport == True:
    write_cif(struct+'-4-FinalBulk.cif', bulk_configuration)