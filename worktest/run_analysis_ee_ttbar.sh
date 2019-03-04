#!/usr/bin/env bash

#NOTE: The command heppy [output_directory] analysis.py -N [# events]
#works for FCC sourced in v0.9 in the terminal

# srcFCCgen and heppy init

#echo "sourcing FCCSW 0.8 (gen)"
#source /cvmfs/fcc.cern.ch/sw/0.8.1/init_fcc_stack.sh
echo "sourcing FCCSW 0.9 (ana)"
source /cvmfs/fcc.cern.ch/sw/views/releases/0.9.1/x86_64-slc6-gcc62-opt/setup.sh

cd ~/FCCee/heppy/
echo "sourcing heppy (init)"
source ./init.sh
cd ~/FCCee/heppy/worktest

echo "running analysis"
# run analysis:
ENDLOOP=10
NEVENTS=10000
for i in $(seq 1 $ENDLOOP); do
    echo "executing heppy $i/$ENDLOOP"
    heppy large_samples/large_sample${i}_init_09 analysis_ee_ttbar_cfg.py -N ${NEVENTS}
done

