# Silicon Quantum ESPRESSO Conversion Example

This directory provides a minimal Quantum ESPRESSO `pw.x` input for silicon to convert configuration to gpawsolve.py's input file by using `converters/qeconverter.py`.

To regenerate the gpawsolve inputs run:

    qeconverter.py --input si.scf.in --output-dir Si-qe --system-name Silicon

Then execute `gpawsolve.py` using the produced files:

    mpirun -np 4 gpawsolve.py -i Silicon.py -g Silicon.cif

