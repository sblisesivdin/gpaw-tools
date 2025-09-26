# Silicon VASP Conversion Example

This example has a minimal VASP input set for silicon to convert configuration to gpawsolve.py's input file by using `converters/vaspconverter.py`.

To reproduce the generated files run:

    vaspconverter.py --poscar POSCAR --incar INCAR --kpoints KPOINTS --output-dir Si-vasp --system-name Silicon

Then execute `gpawsolve.py` using the produced files:

    mpirun -np 4 gpawsolve.py -i Silicon.py -g Silicon.cif

