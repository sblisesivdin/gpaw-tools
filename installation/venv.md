---
layout: default
nav_order: 2
title: Venv Installation
parent: installation
---

# Venv installation

**IMPORTANT NOTE:** 
**gpaw-tools** has evolved and is now called **[Nanoworks](https://nanoworks.readthedocs.io/)**! The **gpaw-tools** project began as a script that utilized only ASE and GPAW. Over the course of four years, it evolved into a comprehensive suite leveraging multiple libraries, including ASAP3, Phonopy, Elastic, OpenKIM, and now modern Machine Learning Potentials (MACE, CHGNet, SevenNet). **Please use [Nanoworks](https://nanoworks.readthedocs.io/) for your further studies.**
{: .text-red-200 }

## Preparing Linux OS

Linux distributions are following a new standard (PEP-668) after 2022/23 to prevent accidentally installing software using pip in a global location by default. This helps avoid clashes between the system's package manager and Python's package manager (pip).  For more information, see the [related PEP-668 documentation](https://packaging.python.org/en/latest/specifications/externally-managed-environments/#externally-managed-environments).

With up-to-date Linux distributions, you must install ASE/GPAW/gpaw-tools in virtual environments. The easiest way to use virtual environments with Python is Venv.

Here, we are giving instructions for Ubuntu Linux. You can directly install or use WSL in Windows OS. For Debian Linux, the steps are nearly the same, and for other distributions, the installation of packages is very similar and straightforward. After [installing Ubuntu on your PC](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview), you need to update and upgrade before continuing:

    $ sudo apt update
    $ sudo apt upgrade

Then, you must install the needed Python packages:

You need the Tk library for GUI, unzip for file unzipping, VENV for virtual environments, and further package installations; we need a PIP installer.

    $ sudo apt install python3-tk python3-venv python3-pip unzip python-is-python3
    
## Preparing and using Virtual Environment

After installing the `python3-venv` package, you can now create and use virtual environments easily. To create an environment named `gpawenv` (you can give a name whatever you like):

    $ python3 -m venv ~/gpawenv

And to activate it:

    $ source ~/gpawenv/bin/activate

## Installation of ASE and GPAW

After preparing your Linux system and environment, you must have the `ase` and `gpaw` codes on your computer. You can find more information about installing [ASE](https://wiki.fysik.dtu.dk/ase/install.html) and [GPAW](https://wiki.fysik.dtu.dk/gpaw/install.html) from their related sites.

Install ASE and other math, parallel, dev libraries

    (gpawenv) $ pip3 install --upgrade ase
    (gpawenv) $ sudo apt install python3-dev libopenblas-dev libxc-dev libscalapack-mpi-dev libfftw3-dev

Create a `siteconfig.py` file:

```
(gpawenv) $ mkdir -p ~/.gpaw
(gpawenv) $ cat > ~/.gpaw/siteconfig.py
fftw = True
scalapack = True
libraries = ['xc', 'blas', 'fftw3', 'scalapack-openmpi']
^D
```

NOTE: If the user wants to use exchange correlations listed in [libxc library](https://www.tddft.org/programs/libxc/), 'xc' must be listed in the libraries line.
{: .text-red-200 }


Then install gpaw

    (gpawenv) $ pip3 install --upgrade gpaw

Use `gpaw info` to see installation information. However, PAW datasets are not installed yet. To install them, first create a directory under `~/.gpaw` and then install PAW datasets.

    (gpawenv) $ mkdir ~/.gpaw/gpaw-setups

for older GPAWs:

    (gpawenv) $ gpaw install-data ~/.gpaw/gpaw-setups/

for GPAW v25.7.0 and later:

    (gpawenv) $ gpaw install-data --gpaw ~/.gpaw/gpaw-setups/

## Installation of ASAP and KIM for Quick Optimization

For quick optimization, we need simple interatomic modeling. For this, we need [ASAP3](https://wiki.fysik.dtu.dk/asap/) for ASE, then we must use [KIM](https://openkim.org/kim-api/) with [OpenKIM](https://openkim.org/) models and [kimpy](https://github.com/openkim/kimpy) libraries.

    (gpawenv) $ pip3 install --upgrade asap3
    (gpawenv) $ sudo apt-get install libkim-api-dev openkim-models libkim-api2 pkg-config
    (gpawenv) $ pip3 install --upgrade kimpy
     
Now, to continue to install `gpaw-tools` first you must deactivate and then again activate the virtual environment to set up the correct PATH values:

    (gpawenv) $ deactivate

or if it is not working try,

   (gpawenv) $ source deactivate

then

    $ source ~/gpawenv/bin/activate

Then you can continue on [installation of gpaw-tools](installationofgpawtools.md)
