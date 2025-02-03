# gpaw-tools
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Issues:](https://img.shields.io/github/issues/sblisesivdin/gpaw-tools)](https://github.com/sblisesivdin/gpaw-tools/issues)
[![Pull requests:](https://img.shields.io/github/issues-pr/sblisesivdin/gpaw-tools)](https://github.com/sblisesivdin/gpaw-tools/pulls)
[![Latest version:](https://img.shields.io/github/v/release/sblisesivdin/gpaw-tools)](https://github.com/sblisesivdin/gpaw-tools/releases/)
![Release date:](https://img.shields.io/github/release-date/sblisesivdin/gpaw-tools)
[![Commits:](https://img.shields.io/github/commit-activity/m/sblisesivdin/gpaw-tools)](https://github.com/sblisesivdin/gpaw-tools/commits/main)
[![Last Commit:](https://img.shields.io/github/last-commit/sblisesivdin/gpaw-tools)](https://github.com/sblisesivdin/gpaw-tools/commits/main)
## Introduction
*gpaw-tools* is a powerful and user-friendly UI/GUI tool for conducting Density Functional Theory (DFT) and molecular dynamics (MD) calculations. Our goal is to make DFT and MD calculations more accessible and easy to use for individuals and small groups, by providing a simple command-line interface and graphical user interface.

The *gpaw-tools* package is built on top of the ASE, ASAP3, KIM-API, PHONOPY, and GPAW libraries, which are well-established and widely used in the scientific community. It allows users to simulate the properties of materials, optimize structures, investigate chemical reactions and processes, and perform calculations on systems with many atoms. With gpaw-tools, researchers, students, and engineers in various fields, including materials science, chemistry, physics, and engineering, can easily conduct DFT and MD calculations and explore the electronic, optical, and phonon structure of material systems. We are constantly working to improve and expand the capabilities of *gpaw-tools*, and we welcome feedback and contributions from the community.

`gpaw-tools` have:
1. The main solver code `gpawsolver.py` can run in PW or LCAO mode. It can perform structure optimization, equation of state and elastic tensor calculations, use several different XCs (as well as hybrid XCs) for spin-polarized DOS and band structure calculations, electron densities, phonon calculations, and optical properties (RPA and BSE). In addition to calculations, it can draw DOS and band structures, save all data, and figure in an ordered way.
2. A force-field quick optimization script `asapsolve.py` for MD calculations using ASAP3 with OpenKIM potentials.
3. To choose better cut-off energy, lattice parameter, and k-points, there are 4 scripts called `optimize_cutoff.py`, `optimize_kpoints.py`, `optimize_kptsdensity.py`, and `optimize_latticeparam.py`.
4. A simple Graphical User Interface (GUI) for gpawsolve.py (and also you may say that GUI for GPAW) which is called `gg.py`.

## Usage
### Installation
You need to install many packages to run `gpaw-tools` successfully. Please refer to the main [installation](https://sblisesivdin.github.io/gpaw-tools/installation) web page for more.

### gpawsolve.py
This is the main code for easy and ordered PW/LCAO Calculations with ASE/GPAW. It can run as a command.

Command line usage: `gpawsolve.py -v -e -d -h -i <inputfile.py> -g <geometryfile.cif>`

Argument list:
```
-g, --geometry    : Use a CIF file for geometry
-i, --input       : Use an input file for variables (input.py) If you do not use this argument, parameters 
                    will be taken from the related lines of gpawsolve.py. Visit the "Input File Keywords" webpage for more.
-e, --energymeas  : Energy consumption measurement. This feature only works with Intel CPUs after the Sandy Bridge generation.
                    Results will be written in a file in the results folder (as kWh!).
-h, --help        : Help
-d, --drawfigures : Draws DOS and band structure figures at the end of the calculation.
-v, --version     : Version information of running code and the latest stable code. Also gives a download link.
```

Instead of using a geometry file, you can put an ASE Atoms object into your input file for the geometry. As an example please note the example at: `examples\Bulk-GaAs-noCIF` folder.
 
 #### How to run?
 Change `<core_number>` with core numbers to use. For getting maximum performance from your PC you can use `total number of cores - 1` or `total RAM/2Gb` as a `<core_number>`. For CPUs supporting hyperthreading, users can use more than one instance of `gpawsolve.py` to achieve maximum efficiency. 

Usage:
`$ mpirun -np <core_number> gpawsolve.py <args>`

or

`$ gpaw -P<core_number> python /path/to/gpawsolve.py -- <args>`

#### Calculation selector (Not complete, not up-to-date information)

| Method | XCs                 | Structure optim. | Spin polarized | Ground | Elastic | DOS | DFT+U | Band | Electron Density | Optical |
| ------ | ------------------- | ---------------- | -------------- | ------ | ------- | --- | ----- | ---- | ---------------- | ------- |
|   PW   | Local and LibXC     | Yes              | Yes            | Yes    | Yes     | Yes | Yes   | Yes  | Yes              | Yes     |
|   PW   | GLLBSC / M          | No               | Yes            | Yes    | Yes     | Yes | No    | Yes  | Yes              | Yes     |
|   PW   | HSE03, HSE06        | No               | Yes            | Yes    | n/a     | Yes | No    | No   | No               | No      |
| PW-G0W0| Local and LibXC     | No               | No             | Yes    | No      | No  | No    | Some | No               | No      |
|  LCAO  | Local and LibXC     | No               | Yes            | Yes    | Yes     | Yes | Yes   | Yes  | Yes              | No      |

*: Just some ground state energy calculations.

### gg.py
Basic DFT calculations can be done graphically with the script `gg.py`. This script behaves as a GUI to run `gpawsolve.py` script. To execute the GUI, type simply:

`$ gg.py`

### asapsolve.py
The inter-atomic potential is a useful tool to perform a quick geometric optimization of the studied system before starting a precise DFT calculation. The `asapsolve.py` script is written for geometric optimizations with inter-atomic potentials. The bulk configuration of atoms can be provided by the user given as a CIF file. A general potential is given for any calculation. However, the user can provide the necessary OpenKIM potential by changing the related line in the input file.

Mainly, `asapsolve.py` is not related to GPAW. However, it is dependent on ASAP3/OpenKIM and Kimpy. Therefore, the user must install the necessary libraries before using the script. Please refer to [related page](https://sblisesivdin.github.io/gpaw-tools/installation/ubuntu/#installation-of-asap-and-kim-for-quick-optimization) for the installation needs.

The main usage is:

`$ asapsolve.py <args>`

#### Arguments

`asapsolve.py -v -h -i <inputfile.py> -g <geometryfile.cif>`

Argument list:
```
-g, --geometry   : Use a CIF file for geometry
-i, --input      : Use an input file for variables (input.py) 

-h --help        : Help
-v --version     : Version information of running code and the latest stable code. It also gives a download link.
```

### optimizations/optimize_cutoff (and kpoints)(and kptsdensity)(and latticeparam).py
Users must provide an ASE Atoms object and simply insert the object inside these scripts. With the scripts, the user can do convergence tests for cut-off energy, k-points, and k-point density and can calculate the energy-dependent lattice parameter values. These codes are mainly based on Prof. J. Kortus, and R. Wirnata's Electr. Structure & Properties of Solids course notes and GPAW's tutorials. Scripts can easily be called with MPI:

    gpaw -P<core_number> python optimize_cutoff.py -- Structure.cif
    gpaw -P<core_number> python optimize_kpoints.py -- Structure.cif
    gpaw -P<core_number> python optimize_kptsdensity.py -- Structure.cif
    gpaw -P<core_number> python optimize_latticeparam.py -- Structure.cif
    
`optimize_latticeparam.py` can perform simultaneous calculation for lattice parameters a and c. And can also draw a 3D contour graph for Energy versus lattice parameters (a and c).

## examples/
There are [some example calculations](https://github.com/sblisesivdin/gpaw-tools/tree/main/examples) given with different usage scenarios. Please send us more calculations to include in this folder.

## Input File Keywords
Many keywords can be used in input files. You can find more at [here](https://sblisesivdin.github.io/gpaw-tools/development/inputfilekeywords/)

## Release notes
Release notes are listed [here](https://sblisesivdin.github.io/gpaw-tools/development/releasenotes/).

## Citing
Please do not forget that gpaw-tools is UI/GUI software. For the main DFT calculations, it uses ASE and GPAW. It also uses the Elastic python package for elastic tensor solutions and ASAP with the KIM database for interatomic interaction calculations and Phonopy for the phonon calculations. Therefore, you must know what you use, and cite them properly. Here, the basic citation information of each package is given.

### ASE 
* Ask Hjorth Larsen et al. "[The Atomic Simulation Environment—A Python library for working with atoms](https://doi.org/10.1088/1361-648X/aa680e)" J. Phys.: Condens. Matter Vol. 29 273002, 2017.
### GPAW
* J. J. Mortensen, L. B. Hansen, and K. W. Jacobsen "[Real-space grid implementation of the projector augmented wave method](https://doi.org/10.1103/PhysRevB.71.035109)" Phys. Rev. B 71, 035109 (2005) and J. Enkovaara, C. Rostgaard, J. J. Mortensen et al. "[Electronic structure calculations with GPAW: a real-space implementation of the projector augmented-wave method](https://doi.org/10.1088/0953-8984/22/25/253202)" J. Phys.: Condens. Matter 22, 253202 (2010).
### KIM
* E. B. Tadmor, R. S. Elliott, J. P. Sethna, R. E. Miller, and C. A. Becker "[The Potential of Atomistic Simulations and the Knowledgebase of Interatomic Models](https://doi.org/10.1007/s11837-011-0102-6)" JOM, 63, 17 (2011).
### Elastic
* P.T. Jochym, K. Parlinski and M. Sternik "[TiC lattice dynamics from ab initio calculations](https://doi.org/10.1007/s100510050823)", European Physical Journal B; 10, 9 (1999).
### Phonopy
* A. Togo "[First-principles Phonon Calculations with Phonopy and Phono3py](https://doi.org/10.7566/JPSJ.92.012001)", Journal of the Physical Society of Japan, 92(1), 012001 (2023).

And for `gpaw-tools` usage, please use the following citation:

* S.B. Lisesivdin, B. Sarikavak-Lisesivdin "[gpaw-tools – higher-level user interaction scripts for GPAW calculations and interatomic potential based structure optimization](https://doi.org/10.1016/j.commatsci.2022.111201)" Comput. Mater. Sci. 204, 111201 (2022).

Many other packages need to be cited. With GPAW, you may need to cite LibXC or cite for LCAO, TDDFT, and linear-response calculations. Please visit their pages for many other citation possibilities. For more you can visit [https://wiki.fysik.dtu.dk/ase/faq.html#how-should-i-cite-ase](https://wiki.fysik.dtu.dk/ase/faq.html#how-should-i-cite-ase), [https://wiki.fysik.dtu.dk/gpaw/faq.html#citation-how-should-i-cite-gpaw](https://wiki.fysik.dtu.dk/gpaw/faq.html#citation-how-should-i-cite-gpaw), and [https://openkim.org/how-to-cite/](https://openkim.org/how-to-cite/).

## Licensing
This project is licensed under the terms of the [MIT license](https://opensource.org/licenses/MIT).
