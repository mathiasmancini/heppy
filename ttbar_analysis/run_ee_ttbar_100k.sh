#!/usr/bin/env bash

echo "sourcing FCCSW 0.8 (gen)"
source /cvmfs/fcc.cern.ch/sw/0.8.1/init_fcc_stack.sh

cd ~/user/mmancini/testFCC/Nicolo/heppy/
echo "Sourcing heppy"
cd ~/user/mmancini/testFCC/Nicolo/heppy/ttbar_analysis

echo "Running the pythia ee_ttbar_100k.txt gen_card"
fcc-pythia8-generate ~/user/mmancini/testFCC/Nicolo/heppy/ttbar_analysis/ee_ttbar_100k.txt
