---
layout: default
nav_order: 5
title: General Usage
---

# General Usage

**IMPORTANT NOTE:** 
**gpaw-tools** has evolved and is now called **[Nanoworks](https://nanoworks.readthedocs.io/)**! The **gpaw-tools** project began as a script that utilized only ASE and GPAW. Over the course of four years, it evolved into a comprehensive suite leveraging multiple libraries, including ASAP3, Phonopy, Elastic, OpenKIM, and now modern Machine Learning Potentials (MACE, CHGNet, SevenNet). **Please use [Nanoworks](https://nanoworks.readthedocs.io/) for your further studies.**
{: .text-red-200 }

When you download `gpaw-tools` from GitHub and extract it to a folder you will have a folder structure as:

```
gpaw-tools/
├── examples/
├── optimizations/
│   ├── optimize_cutoff.py
│   ├── optimize_kpoints.py
│   ├── optimize_kptsdensity.py
│   └── optimize_latticeparam.py
├── gui_files/
└── asapsolve.py
└── gpawsolve.py
└── gg.py
└── shrinkgpw.py
```

## gpawsolve.py
This is the main script for easy and ordered PW/LCAO Calculations with ASE/GPAW. It can run as a stand-alone script or as a command.

### As a command:
Command line usage: `gpawsolve.py -v -e -d -h -i <inputfile.py> -g <geometryfile.cif>`

Argument list:
```
-g, --geometry    : Use a CIF file for geometry
-i, --input       : Use an input file for variables (input.py) If you do not use this argument, parameters 
                    will be taken from the related lines of gpawsolve.py. Visit the "Input File Keywords" webpage for more. 
-e, --energymeas  : Energy consumption measurement. This feature only works with Intel CPUs after the Sandy Bridge generation.
                    Results will be written in a file in the results folder (in kWh!).
-h --help         : Help
-d --drawfigures  : Draws DOS and band structure figures at the end of the calculation.
-v --version      : Version information of running code and the latest stable code. It also gives a download link.
 ```
 
 You can put the ASE Atoms object into your config file and therefore can use it like an input file. As an example please note the example in: `examples\Bulk-GaAs-noCIF` folder.
 
### How to run?
Change `<core_number>` with core numbers to use. For getting maximum performance from your PC you can use `total number of cores - 1` or `total RAM/2Gb` as a `<core_number>`. For CPUs supporting hyperthreading, users can use more than one instance of `gpawsolve.py` to achieve maximum efficiency. 

Usage:
`$ mpirun -np <core_number> gpawsolve.py <args>`

or

`$ gpaw -P<core_number> python /path/to/gpawsolve.py -- <args>`

### Calculation selector (Not complete, not up-to-date information)

 | Method | XCs                 | Structure optim. | Spin polarized | Ground | Elastic | DOS | DFT+U | Band | Electron Density | Optical |
 | ------ | ------------------- | ---------------- | -------------- | ------ | ------- | --- | ----- | ---- | ---------------- | ------- |
 |   PW   | Local and LibXC     | Yes              | Yes            | Yes    | Yes     | Yes | Yes   | Yes  | Yes              | Yes     |
 |   PW   | GLLBSC / M          | No               | Yes            | Yes    | Yes     | Yes | No    | Yes  | Yes              | Yes     |
 |   PW   | HSE03, HSE06        | No               | Yes            | Yes    | n/a     | Yes | No    | No   | No               | No      |
 | PW-G0W0| Local and LibXC     | No               | No             | Yes    | No      | No  | No    | Some | No               | No      |
 |  LCAO  | Local and LibXC     | Yes              | Yes            | Yes    | Yes     | Yes | Yes   | Yes  | Yes              | No      |

*: Just some ground state energy calculations for PBE0 and HSE06.

## gg.py
Basic DFT calculations can be done graphically with the script `gg.py`. This script behaves as a GUI to run the `gpawsolve.py` script. To execute the GUI, type simply:
  gg.py

## asapsolve.py
The inter-atomic potential is a useful tool to perform a quick geometric optimization of the studied system before starting a precise DFT calculation. The `asapsolve.py` script is written for geometric optimizations with inter-atomic potentials. The bulk configuration of atoms can be provided by the user given as a CIF file. A general potential is given for any calculation. However, the user can provide the necessary OpenKIM potential by changing the related line in the input file.

Mainly, `asapsolve.py` is not related to GPAW. However, it is dependent on ASAP3/OpenKIM and Kimpy. Therefore, the user must install the necessary libraries before using the script. Please refer to [related page](https://www.lrgresearch.org/gpaw-tools/installation/ubuntu/#installation-of-asap-and-kim-for-quick-optimization) for the installation needs.

The main usage is:

`$ asapsolve.py <args>`

### Arguments

`asapsolve.py -v -h -i <inputfile.py> -g <geometryfile.cif>`

Argument list:
```
-g, --geometry   : Use a CIF file for geometry
-i, --input      : Use an input file for variables (input.py) 

-h --help        : Help
-v --version     : Version information of running code and the latest stable code. It also gives a download link.
 ```
 
## optimizations/optimize_cutoff (and kpoints)(and latticeparam).py
Users must provide an ASE Atoms object and simply insert the object inside these scripts. With the scripts, the user can do convergence tests for cut-off energy, and k-points and can calculate the energy-dependent lattice parameter values. These codes are mainly based on Prof. J. Kortus, R. Wirnata's Electr. Structure & Properties of Solids course notes and GPAW's tutorials. Scripts can easily be called with MPI:

    gpaw -P <core_number> python optimize_cutoff.py
    gpaw -P <core_number> python optimize_kpoints.py
    gpaw -P <core_number> python optimize_latticeparam.py

`optimize_latticeparam.py` can perform simultaneous calculations for lattice parameters a and c. And can also draw a 3D contour graph for Energy versus lattice parameters (a and c).

## examples/
There are some example calculations given with different usage scenarios in the code. Please send us more calculations to include.

### GPAW Example List

| Name              | Notes  | 
| ----------------- | ------ |
| Bulk-GaAs-noCIF   | Ground, DOS, and Band calculations of Bulk GaAs with PW. Positions are given with Atom object.          |
| Cr2O-spin         |Spin-dependent electronic properties of CrO2 |
| Graphene-LCAO     | Pristine graphene and graphene with a defect with LCAO. Uses a single config for two calculations. |
| MoS2-GW           | GW Approximation calculation for MoS2 |
| Si-2atoms-optical | Three-step calculation. First step ground, DOS, and Band calculations. Second and third steps for RPA and BSE optical calculations, respectively. The structure is given with a CIF file. |
| ZnO with DFT+U    | Wurtzite ZnO calculation with DFT+U. Positions are given with a Bulk object. Hubbard params are O-p: 7eV, Zn-d: 10eV|
| TiC-elastic-electronic | Elastic (EoS and Elastic Tensor) and Electronic Properties of Rocksalt TiC |
| Si-with-HSE | Ground state, DOS, and band structure of Si with HSE06 Hybrid XC | 

### ASAP3 Example List

| Name              | Notes  | 
| ----------------- | ------ |
| ASAP3-Example     | Germanene nanosheet example with a general potential.          |
