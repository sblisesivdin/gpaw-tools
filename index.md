---
layout: default
nav_order: 1
title: Home
---
# Welcome to *gpaw-tools*
{: .fs-9 }

{: .important }

> **gpaw-tools** has evolved and is now called **[Nanoworks](https://nanoworks.readthedocs.io/)**!

> The **gpaw-tools** project began as a script that utilized only ASE and GPAW. Over the course of four years, it evolved into a comprehensive suite leveraging multiple libraries,

> including ASAP3, Phonopy, > Elastic, OpenKIM, and now modern Machine Learning Potentials (MACE, CHGNet, SevenNet).

> Please use [Nanoworks](https://nanoworks.readthedocs.io/){: .btn .btn-purple } for your further studies.

`gpaw-tools` is a powerful and user-friendly tool for running Density Functional Theory (DFT) and molecular dynamics (MD) simulations. It provides both a simple command-line interface and a graphical user interface (GUI), aiming to make DFT/MD calculations more accessible to individuals and small research groups. It leverages well-established libraries – **ASE**, **ASAP3**, **Elastic**, **KIM-API**, **Phonopy**, and **GPAW** – as its computational backends​. This integration allows users to simulate material properties, optimize structures, investigate chemical reactions, and perform calculations on systems with many atoms. Researchers and students in fields such as materials science, chemistry, and physics can explore the electronic, optical, and phonon properties of materials without requiring extensive programming expertise. The tool can also produce useful visual outputs, such as potential energy surfaces, electronic band structures, and density of states plots, as shown in the examples below​

![Image](assets/images/banner.png)

Key features of `gpaw-tools` include a primary solver script for DFT calculations, a quick force-field optimization module for pre-relaxation, several utility scripts for convergence testing, and a simple GUI for easier use. In practice, this means you can perform common tasks like geometry optimization, equation-of-state calculations, elastic constant calculations, spin-polarized density of states and band structure analysis, phonon spectrum computations, and even basic optical property calculations (RPA/BSE) with relative ease. The graphical interface further lowers the barrier for new users by allowing basic DFT calculations to be set up and run without manual scripting. `gpaw-tools` is an open-source project (MIT licensed) under active development. It is continually improved with new features and enhancements, and feedback from the community is welcome. Whether you prefer using the command-line or a GUI, `gpaw-tools` offers a convenient higher-level interface to powerful simulation engines, aiming to streamline computational workflows for material science research.

{: .fs-6 .fw-300 }

[Download now](#download){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/sblisesivdin/gpaw-tools){: .btn .fs-5 .mb-4 .mb-md-0 }

`gpaw-tools` have:
1. The main solver script `gpawsolve.py` can run in PW or LCAO mode. It can perform structure optimization, equation of state, and elastic tensor calculations, and use several different XCs (as well as hybrid XCs) for spin-polarized DOS and band structure calculations, electron densities, phonon calculations, and optical properties (RPA and BSE). In addition to calculations, it can draw DOS and band structures, save all data, and present the data in an orderly way.
2. A force-field quick optimization script, `asapsolve.py`, for MD calculations using ASAP3 and OpenKIM potentials. 
3. To choose better cut-off energy, lattice parameter, and k-points, there are 4 scripts called `optimize_cutoff.py`, `optimize_kpoints.py`,`optimize_kptsdensity.py`, and `optimize_latticeparam.py`.
4. A simple Graphical User Interface (GUI) for `gpawsolve.py` is called `gg.py`.
5. Simple input file conversion scripts for VASP and QE input files.

More information about [gpaw-tools idea](about.md), [installation](installation/installation.md), [usage](generalusage.md), and [release notes](development/releasenotes.md) can be found at related pages.

## Download

**Latest stable release: v25.10.0 [download (tar.gz)](https://github.com/sblisesivdin/gpaw-tools/archive/refs/tags/v25.10.0.tar.gz), [download (zip)](https://github.com/sblisesivdin/gpaw-tools/archive/refs/tags/v25.10.0.zip)**

Latest development release: [download (tar.gz)](https://github.com/sblisesivdin/gpaw-tools/archive/refs/heads/main.tar.gz), [download (zip)](https://github.com/sblisesivdin/gpaw-tools/archive/refs/heads/main.zip)

## News
* **[gpaw-tools](development/releasenotes.md#version-25100)** version 25.10.0 released. There are many fixes. Phonon calculations, `gg.py`, were broken. They are all fixed. For MD calculations, `asapsolve.py` has new features. New input file conversion scripts for VASP and QE input files are added in this release (October 1, 2025).
* **[gpaw-tools](development/releasenotes.md#version-2540)** version 25.4.0 released. This version has a rewritten elastic calculation part. Now it can calculate elastic calculations of bulk and 2D structures successfully (April 18, 2025).
* **[gpaw-tools](development/releasenotes.md#version-2521)** version 25.2.1 released. This version is working fine with GPAW 25.1.0. For nearly a year, optical calculations have not been done due to code changes in GPAW. Now, with this release, optical calculations are working as as possible they can. There is no v25.2.0. Version v25.2.1 is a minor correction over it (February 3, 2025).
* As our lab has had [an institutional website](https://avesis.gazi.edu.tr/arastirma-grubu/lrg/) for the last year, we will close lrgresearch.org and GitHub relations shortly. Therefore, we have moved gpaw-tools and several other repositories of Prof. Lisesivdin to [sblisesivdin.github.io](https://sblisesivdin.github.io). As a result, the legal address of gpaw-tools is now [https://sblisesivdin.github.io/gpaw-tools](https://sblisesivdin.github.io/gpaw-tools). We apologize for any inconvenience this may have caused (January 22, 2025).
* **[gpaw-tools](development/releasenotes.md#version-2461)** version 24.6.1 released. This is a quick-fix release. Because SPGlib dropped the ASE-type Atoms object after version 2.2.0, `gpawsolve.py` started to give an error. ASE will maintain the `get_spacegroup()` function call going forward. With this change, `gpawsolve.py` no longer requires the `spglib` package.
* **[gpaw-tools](development/releasenotes.md#version-2460)** version 24.6.0 released. This version is compatible with newer versions of > ASE 3.23.0 and GPAW 24.6.0 (June 5, 2024).
* **[gpaw-tools](development/releasenotes.md#version-23100)** version 23.10.0 released (October 13, 2023).
* **[gpaw-tools](development/releasenotes.md#version-2370)** version 23.7.0 released. It is a version with major changes, and **you need to add a new keyword `Ground_calc` to your old input files**. Please use the input files in the example folder to create new input files. This version has many new features: Phonon calculations, energy consumption measurement, etc. Please refer to [release notes](development/releasenotes.md#version-2370). (July 4, 2023)
* **[gpaw-tools](development/releasenotes.md#version-2320)** version 23.2.0 released. It is a version with major changes that is **incompatible with the previous versions**. Please use the input files in the example folder to create new input files (February 1, 2023).
* A new oral presentation about *gpaw-tools* is presented at MSNG2022 (September 22, 2022).
* We had a small department-wide hands-on activity about installing and using ASE, GPAW, and gpaw-tools software at Gazi University's Department of Physics (August 8, 2022). 
* **[gpaw-tools](development/releasenotes.md#version-2270)** version 22.7.0 released (July 12, 2022).
* A new poster presentation about *gpaw-tools* will be presented at the 2022 Workshop on Recent Developments in Electronic Structure (June 2, 2022).
* **[gpaw-tools](development/releasenotes.md#version-2250)** version 22.5.0 released (May 8, 2022).
* **[gpaw-tools](development/releasenotes.md#version-2240)** version 22.4.0 released (Apr 7, 2022).
* **[gpaw-tools](development/releasenotes.md#version-2230)** version 22.3.0 released (Mar 4, 2022).
* Our [paper](https://doi.org/10.1016/j.commatsci.2022.111201) about *gpaw-tools* is published in Computational Material Science.
* **[gpaw-tools](development/releasenotes.md#version-21120)** version 21.12.0 released (Dec 2, 2021).
* **[gpaw-tools](development/releasenotes.md#version-21110)** version 21.11.0 released (Nov 2, 2021).
* **[gpaw-tools](development/releasenotes.md#version-21101)** version 21.10.1 released (Oct 1, 2021).
* **[gpaw-tools](development/releasenotes.md#version-21100)** version 21.10.0 released (Oct 1, 2021).
* **[gpaw-tools](development/releasenotes.md#version-2190)** version 21.9.0 released (Sep 14, 2021).

## Citing
Please do not forget that gpaw-tools is UI/GUI software. The main DFT calculations use ASE and GPAW. It also uses the Elastic python package for elastic tensor solutions and ASAP with the KIM database for interatomic interaction calculations and Phonopy for phonon calculations. Therefore, you must know what you use and cite them properly. Here, the basic citation information of each package is given.

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
