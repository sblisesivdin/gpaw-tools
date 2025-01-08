#!/usr/bin/env bash
echo "gpaw-tools: "
echo "Adding all examples to tsp queue. Please use tsp after running this."
CORENUMBER=4
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
# Examples
# Bulk-Al-noCIF -------------------
echo "Adding: Bulk-GaAs-noCIF"
cd ./Bulk-GaAs-noCIF
tsp mpirun -np $CORENUMBER gpawsolve.py -i bulk_gaas.py

# Cr2O-spin -------------------
echo "Adding: Cr2O-spin"
cd ../Cr2O-spin
tsp mpirun -np $CORENUMBER gpawsolve.py -i Cr2O.py -g Cr2O_mp-1206821_primitive.cif

# Graphene-LCAO -------------
echo "Adding: Graphene-LCAO"
cd ../Graphene-LCAO
echo "Step 1: Pristine graphene"
tsp mpirun -np $CORENUMBER gpawsolve.py -i graphene.py -g graphene4x4.cif
echo "Step 2: Graphene with defect"
tsp mpirun -np $CORENUMBER gpawsolve.py -i graphene.py -g graphene4x4withdefect.cif

# Graphene-charged -------------
echo "Adding: Graphene-charged"
cd ../Graphene-charged
echo "Step 1: Neutral defected graphene"
tsp mpirun -np $CORENUMBER gpawsolve.py -i graphene-neutral.py -g graphene4x4withdefect.cif
echo "Step 2: Charged defected Graphene"
tsp mpirun -np $CORENUMBER gpawsolve.py -i graphene-charged.py -g graphene4x4withdefect.cif

# Not working after GPAW 22.1.0, needs future fix.
# MoS2-GW -------------------
#echo "Adding: MoS2-GW"
#cd ../MoS2-GW
#tsp gpawsolve.py -o -i MoS2-GW.py -g MoS2-structure.cif

# Si-2atoms-optical ----------------
echo "adding: Si-2atoms-optical"
cd ../Si-2atoms-optical
echo "Step 1: Ground, DOS and Band"
tsp mpirun -np $CORENUMBER gpawsolve.py -i Si-Step1-ground_dos_band.py -g Si_mp-149_primitive_Example.cif
echo "Step 2: Optical - RPA"
tsp gpawsolve.py -i Si-Step2-optical-RPA.py -g Si_mp-149_primitive_Example.cif
echo "Step 3: Optical - BSE"
tsp gpawsolve.py -i Si-Step3-optical-BSE.py -g Si_mp-149_primitive_Example.cif

# Wurtzite ZnO with DFT+U
echo "Adding: ZnO with DFT+U"
cd ../ZnO-with-Hubbard
echo "Step 1: Ground, DOS and Band with DFT+U"
tsp mpirun -np $CORENUMBER gpawsolve.py -i ZnO_withHubbard.py
echo "Step 2: Ground, DOS and Band without DFT+U"
tsp mpirun -np $CORENUMBER gpawsolve.py -i ZnO_woHubbard.py

# Rocksalt TiC with Elastic Calculations
echo "Adding: Rocksalt TiC"
cd ../TiC-elastic-electronic
tsp mpirun -np $CORENUMBER gpawsolve.py -i TiC.py -g TiC_mp-631_primitive-Final.cif

# Phonon dispersion of Aluminum
echo "Adding: Phonon dispersion of bulk Aluminum"
cd ../Al-phonon
tsp mpirun -np $CORENUMBER gpawsolve.py -i Al-phonon.py -g Al_mp-134_primitive.cif

# Finish
echo "All calculations except the HSE calculation are added. Due to consuming to much time, please run HSE example seperately."
