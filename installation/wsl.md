---
layout: default
nav_order: 4
title: Installation on WSL
parent: installation
---

# Installation on WSL

**IMPORTANT NOTE:** 
**gpaw-tools** has evolved and is now called **[Nanoworks](https://nanoworks.readthedocs.io/)**! The **gpaw-tools** project began as a script that utilized only ASE and GPAW. Over the course of four years, it evolved into a comprehensive suite leveraging multiple libraries, including ASAP3, Phonopy, Elastic, OpenKIM, and now modern Machine Learning Potentials (MACE, CHGNet, SevenNet). **Please use [Nanoworks](https://nanoworks.readthedocs.io/) for your further studies.**
{: .text-red-200 }

## Installation on a Windows 10 system (with WSL1)
This installation note explains how to install WSL1 and other required tools to study gpaw-tools on a Windows 10 system. WSLg is coming by default with Windows 11, and the installation note for Windows 11 explains similar things, but using WSLg. If you are using Windows 11, please continue from here.
We are suggesting Ubuntu 20.04 LTS version for *gpaw-tools* studies.

### WSL Version Control
[After activating the WSL](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10), and installing an Ubuntu system for the Microsoft Store application, we need to control the WSL version of the Linux distribution installed in your system. Open PowerShell and type:

    wsl --list --verbose 

The result will be something like:

    NAME            STATE           VERSION
    Ubuntu-20.04    Running         1

Your WSL distribution version must be "1", not "2". If it is not, change the WSL distribution version with the command:

    wsl --set-version Ubuntu-20.04 1

### Update, upgrade, and XWindows
Open Ubuntu, finish the installation of it, then update your Linux system with:

    sudo apt update
    sudo apt upgrade
    
To use an X server on Windows, firstly, you need to install a few files (not necessary if you do not use matplotlib features).

    sudo apt install libglu1-mesa-dev freeglut3 freeglut3-dev mesa-common-dev

You also need to install [XMing](https://sourceforge.net/projects/xming/) on Windows. In new WSL installations, the following line must be added to the `~/.bashrc` file. You can use the nano editor to do this:

    nano ~/.bashrc

and add these lines at the end of the file

    export LIBGL_ALWAYS_INDIRECT=0
    export DISPLAY=localhost:0.0

After editing the ~/.bashrc file, quit the current shell session and start a new one (or you can use the `source ~/.bashrc` command).

## Installation on a Windows 11 system (with WSL2 and WSLg)
This installation note explains how to install WSLg and other required tools to study gpaw-tools on a Windows 11 system. WSL2 is coming by default with Windows 11. With WSLg, you will not need to install Xming on your Windows system, and the Ubuntu packages libglu1-mesa-dev, freeglut3, freeglut3-dev mesa-common-dev on your system.
We are suggesting Ubuntu 20.04 LTS version for *gpaw-tools* studies.

Open Ubuntu, finish the installation of it, then update your Linux system with:

    sudo apt update
    sudo apt upgrade
    
You do not need to install an X server on your Windows to use with WSLg. 

### WSL2 memory problem
By default, the WSL2 will consume up to 50% of the total system memory up to 8GB at max. However, it is possible to configure an upper limit for the memory and swap usage. Firstly, you must create a .wslconfig file in your Windows-related home directory (C:\Users\<user>). And for 14GB RAM and 32 GB Swap, add the following information to that file:

    [wsl2]
    memory=14GB
    swap=32GB

Then, open PowerShell or terminal and run:

    wsl --shutdown

Then, you can continue with the new RAM-Swap settings.
    
## Installation of ASE and GPAW
After preparing your Linux system, you must have `ase` and `gpaw` codes on your computer. You can find more information about the installation of [ASE](https://wiki.fysik.dtu.dk/ase/install.html) and [GPAW](https://wiki.fysik.dtu.dk/gpaw/install.html) from their related sites.

You need the Tk library for GUI, unzip for file unzipping, and for further package installations, we need a PIP installer

    sudo apt install python3-tk python3-pip unzip python-is-python3

Install ASE and other math, parallel, and dev libraries

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

    gpaw install-data --gpaw ~/.gpaw/gpaw-setups/

## Installation of ASAP and KIM for Quick Optimization

For quick optimization, we need simple interatomic modeling. For this, we need [ASAP3](https://wiki.fysik.dtu.dk/asap/) for ASE, then we must use [KIM](https://openkim.org/kim-api/) with [OpenKIM](https://openkim.org/) models and [kimpy](https://github.com/openkim/kimpy) libraries.

    pip install --upgrade --user ase asap3
    sudo add-apt-repository ppa:openkim/latest
    sudo apt-get update
    sudo apt-get install libkim-api-dev openkim-models libkim-api2 pkg-config
    pip3 install kimpy

Then you can continue on [installation of gpaw-tools](installationofgpawtools.md).

