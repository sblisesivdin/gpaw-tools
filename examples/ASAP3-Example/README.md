# ASAP3 Germanene Example

This directory demonstrates the standalone `asapsolve.py` workflow with ASE/ASAP3 interatomic potentials. Two input files are provided:

- `sampleinput.py` keeps the classic single-temperature run.
- `sampleinput_profiles.py` sweeps temperature, time step, and friction, emitting a result set for every value combination.

## Running the examples

From this directory (both `-i` and `-g` are mandatory):


    asapsolve.py -i sampleinput.py -g germanene1x1_Example.cif


To exercise the profile-based run (which now iterates through all combinations of the listed temperatures, time steps, and frictions, writing separate result files for each):


    asapsolve.py -i sampleinput_profiles.py -g germanene1x1_Example.cif


Each execution writes results into a `<geometry_filename>_results/` folder next to the CIF (for example `germanene1x1_Example_results/germanene1x1_Example-Results.traj`) along with the log, reconstructed `Atoms` module, final CIF, and the energy table.

Tune potentials, temperature schedules, and MD settings by editing the corresponding input file.
