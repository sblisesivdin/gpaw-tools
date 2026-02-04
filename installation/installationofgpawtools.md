---
layout: default
nav_order: 6
title: Installation of gpaw-tools
parent: installation
---

# Installation of gpaw-tools

**IMPORTANT NOTE:** 
**gpaw-tools** has evolved and is now called **[Nanoworks](https://nanoworks.readthedocs.io/)**! The **gpaw-tools** project began as a script that utilized only ASE and GPAW. Over the course of four years, it evolved into a comprehensive suite leveraging multiple libraries, including ASAP3, Phonopy, Elastic, OpenKIM, and now modern Machine Learning Potentials (MACE, CHGNet, SevenNet). **Please use [Nanoworks](https://nanoworks.readthedocs.io/) for your further studies.**
{: .text-red-200 }

After installing ASE, GPAW, ASAP, KIM and other necessary packages, you can proceed with the installation of *gpaw-tools*.

Before, we need to install `setuptools_scm` seperately. Otherwise it can give an error.

     pip3 install setuptools_scm
 
Then, starting to the installation of `gpaw-tools`, we need to install `spglib`, `docutils`, `requests`, `elastic`, and `phonopy` packages and their dependencies. If you used conda to install previous packages, you do not need to run the following commands (If you try to run these two commands as a single command you may have received an error).

   
    pip3 install spglib docutils elastic requests phonopy

If you want to use the energy consumption measurement feature, install:

    pip3 install pyrapl pymongo pandas

Also, lastly, it is good to use a job queue system when you have many inputs to run. GPAW / gpaw-tools can be run with task managers like SLURM. However, if you use your GPAW / gpaw-tools system on your local server/workstation, using Task Spooler is a good idea. It only works on one server for one user. It makes a queue, and runs your commands in order. To install the tsp command to your Ubuntu system, use:

    sudo apt install task-spooler

Now, all needed packages are installed and we can continue with the installation of `gpaw-tools`. In your home folder (~), let's download the latest development release (you can prefer a stable release also, please visit [https://sblisesivdin.github.io/gpaw-tools/](https://sblisesivdin.github.io/gpaw-tools/) to get the latest URL)

    cd ~
    wget https://github.com/sblisesivdin/gpaw-tools/archive/refs/heads/main.zip
    unzip main.zip

All files will be extracted to a folder called `gpaw-tools-main`. We need to make this folder to `~/.bashrc` file to system-wide reach.

    nano ~/.bashrc

Add the following line at the end of your ``~/.bashrc`` file.

    export PATH=/home/YOURUSERNAME/gpaw-tools-main:$PATH

After editing ~/.bashrc file quit the current shell session and start a new one (or you can use `source ~/.bashrc` command). 

IMPORTANT NOTE FOR GPAW 23.6.0: The version 23.6.0 of GPAW has an error when you want to make DOS calculations. There is a line missing in `gpaw/dos.py` file. It is already fixed in the development version, however, if you are using PIP to install gpaw, you will have this error. You can add that line with a single command. You must run this command only ONCE.
{: .text-red-200 }

    sed -i "166i\ \ \ \ \ \ \ \ from gpaw.calculator import GPAW" "$(python -m site --user-site)/gpaw/dos.py"
    
Congratulations! You installed all necessary files to run *gpaw-tools*. You can continue with our [usage](generalusage.md) page, or continue with the `examples` folder in your `gpaw-tools-main` folder. All examples have README.md files.

