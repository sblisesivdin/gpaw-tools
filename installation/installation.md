---
layout: default
nav_order: 3
title: Installation
has_children: true
permalink: /installation
---

# Installation

**IMPORTANT NOTE:** 
**gpaw-tools** has evolved and is now called **[Nanoworks](https://nanoworks.readthedocs.io/)**! The **gpaw-tools** project began as a script that utilized only ASE and GPAW. Over the course of four years, it evolved into a comprehensive suite leveraging multiple libraries, including ASAP3, Phonopy, Elastic, OpenKIM, and now modern Machine Learning Potentials (MACE, CHGNet, SevenNet). **Please use [Nanoworks](https://nanoworks.readthedocs.io/) for your further studies.**
{: .text-red-200 }

These installation notes are based on installations on the Linux operating system. Here, we are using the Ubuntu distro as a Linux system. However, other Linux distros will also work with similar commands. If you are new to Linux, please continue with Ubuntu Linux and our commands given below,

Required software for successfully running *gpaw-tools* software:

* Linux Operating system (can be independently installed, virtually installed, or installed as WSL distro under Windows Operating system)
* Python 3.7 or above (with PIP and TK packages)
* Atomic Simulation Environment (ASE) (will automatically install to NumPy, SciPy, Matplotlib packages)
* GPAW
* BLAS, LibXC, MPI, LibKIM, OpenKIM, and ScaLAPACK packages
* Some other Python packages like Elastic, spglib (not required after gpaw-tools v24.6.1), kimpy, ASAP3, Phonopy.

Linux distributions are following a new standard (PEP-668) after 2022/23 to prevent accidentally installing software using pip in a global location by default. This helps avoid clashes between the system's package manager and Python's package manager (pip).  For more information, please review the [related PEP-668 documentation](https://packaging.python.org/en/latest/specifications/externally-managed-environments/#externally-managed-environments).

**New gpaw-tool installations after v.24.6.1**, must use VENV installation regardless of installed on a standalone Linux or a Linux on a WSL:

* [VENV installation](venv.md)

Older installation information for different systems: 

* [Conda installation](conda.md)
* [Ubuntu Linux Distribution on a Windows System (WSL)](wsl.md)
* [Ubuntu Linux Distribution](ubuntu.md) 

After finishing a proper base for *gpaw-tools*, you can go ahead with the installation information of *gpaw-tools*.

* [Installation of gpaw-tools](installationofgpawtools.md)
