---
layout: default
nav_order: 3
title: Ubuntu Linux Installation
parent: installation
---


# Ubuntu Linux installation

After [installing Ubuntu on your PC](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview), you just need to update and upgrade before continuing:

    sudo apt update
    sudo apt upgrade
    
## Installation of ASE and GPAW

After preparing your Linux system, you must have `ase` and `gpaw` codes on your computer. You can find more information about the installation of [ASE](https://wiki.fysik.dtu.dk/ase/install.html) and [GPAW](https://wiki.fysik.dtu.dk/gpaw/install.html) from their related sites.

You need the Tk library for GUI, unzip for file unzipping, and for further package installations, we need the PIP installer

    sudo apt install python3-tk python3-pip unzip python-is-python3

Install ASE and other math, parallel, dev libraries

    pip3 install --upgrade --user ase
    
At this point, PIP can give some warnings as:

    WARNING: The scripts f2py, f2py3 and f2py3.8 are installed in '/home/YOURUSERNAME/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    WARNING: The scripts ase, ase-build, ase-db, ase-gui, ase-info and ase-run are installed in '/home/YOURUSERNAME/.local/bin' 
    which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

Add the following line at the end of your ``~/.bashrc`` file.

    export PATH=/home/YOURUSERNAME/.local/bin:$PATH
    

After editing the ~/.bashrc file, quit the current shell session and start a new one (or you can use the `source ~/.bashrc` command). Then continue,

    sudo apt install python3-dev libopenblas-dev libxc-dev libscalapack-mpi-dev libfftw3-dev

Create a `siteconfig.py` file:

```
$ mkdir -p ~/.gpaw
$ cat > ~/.gpaw/siteconfig.py
fftw = True
scalapack = True
libraries = ['xc', 'blas', 'fftw3', 'scalapack-openmpi']
^D
```

NOTE: If the user wants to use exchange correlations listed in [libxc library](https://www.tddft.org/programs/libxc/), 'xc' must be listed in the libraries line as shown above.
{: .text-red-200 }


Then install gpaw

    pip3 install --upgrade --user gpaw

NOTE: If the user wants to use gpaw-tools versions 23.7.0 and before, GPAW version 22.8.0 must be used. The above command will be `pip3 install --upgrade --user gpaw==22.8.0`
{: .text-red-200 }

Use `gpaw info` to see installation information. However, PAW-datasets are not installed yet. To install it, firstly create a directory under `~/.gpaw`, then install PAW datasets

    mkdir ~/.gpaw/gpaw-setups

for older GPAWs:

    gpaw install-data ~/.gpaw/gpaw-setups/

for GPAW v25.7.0 and later:

    $ gpaw install-data --gpaw ~/.gpaw/gpaw-setups/

## Installation of ASAP and KIM for Quick Optimization

For quick optimization, we need simple interatomic modelling. For this, we need [ASAP3](https://wiki.fysik.dtu.dk/asap/) for ASE, then we must use [KIM](https://openkim.org/kim-api/) with [OpenKIM](https://openkim.org/) models and [kimpy](https://github.com/openkim/kimpy) libraries.

    pip install --upgrade --user ase asap3
    sudo add-apt-repository ppa:openkim/latest
    sudo apt-get update
    sudo apt-get install libkim-api-dev openkim-models libkim-api2 pkg-config
    pip3 install kimpy

     
Then you can continue on [installation of gpaw-tools](installationofgpawtools.md)

