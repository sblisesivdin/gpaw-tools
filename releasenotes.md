---
layout: default
navigation_weight: 5
title: Release Notes
---

## Release notes

### Development version
#### September 2021
* New argument parsing scheme for better future usages.
* Very basic PW-EXX mode with HSE06 and PBE06. (Only some ground-state calculations.)
* Adding GW0 and G0W0-GW0 selector.
* Adding G0W0 approximation to `gpawsolve.py` (only bands).
* Some small corrections.

### Version 21.9.0

#### September 2021
* Corrected `quickoptimize.py` behaviour.
* Many code quality and folder structure improvements.
* Comment additions to code.
* Better README.md.

#### August 2021
* `gg.py` which is a GUI for gpaw-tools is added to project. It can do all `gpawsolve.py`'s features in a graphical way!
* `gpawsolve.py` can be run solely as a command now (This is needed for a GUI project).
* All three scripts`PW-Electronic.py`, `LCAO-Electronic.py` and `PW-Optical-SingleCoreOnly.py` scripts becomes a single for-all-case script: `gpawsolve.py`.
* `PW-Electronic-changename.py` script becomes `PW-Electronic.py`.
* Spin-polarized results in `PW-Electronic-changename.py` script.
* All-electron density calculations in `PW-Electronic-changename.py`.
* CIF Export in `PW-Electronic-changename.py` script.
* Better parallel computation.
* Several XCs available for PW.
* `LCAO-Electronic.py` script.
* Strain minimization in PW only. 
* BFGS to LBFGS, Small many changes have been done.

#### July 2021 
* `PW-Optical-SingleCoreOnly.py` script for optical calculations.
* `PW-Electronic-changename.py` script for electronic calculations.

#### March 2020 
* First scripts for personal usage.