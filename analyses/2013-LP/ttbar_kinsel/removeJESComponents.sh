#!/bin/bash
# Script to quickly remove the jes components and leave just the JES total
# Ian Connelly 
# 4 Feb 2013

for FILE in `ls *SF*new.txt`; do

    sed -i '/Baseline/d' $FILE
    sed -i '/BJesUnc/d' $FILE
    sed -i '/closeby/d' $FILE
    sed -i '/EtaIntercalibration/d' $FILE
    sed -i '/flavor_comp/d' $FILE
    sed -i '/flavor_response/d' $FILE
    sed -i '/Pile_Mu/d' $FILE
    sed -i '/Pile_NPV/d' $FILE
    # For future iterations, ensure these aren't in the file
    sed -i '/res_soft_pthard' $FILE
    sed -i '/sc_soft_pthard' $FILE
    # New JES cpts from SMWZ setup
    sed -i '/Effective1/d' $FILE
    sed -i '/Effective2/d' $FILE
    sed -i '/Effective3/d' $FILE
    sed -i '/Effective4/d' $FILE
    sed -i '/Effective5/d' $FILE
    sed -i '/Effective6p/d' $FILE
    sed -i '/EtaIntercalibration_Modelling/d' $FILE
    sed -i '/EtaIntercalibration_StatMeth/d' $FILE
    sed -i '/Pileup_Pt/d' $FILE
    sed -i '/Pileup_Rho/d' $FILE
    sed -i '/SingleParticle_HighPt/d' $FILE
    sed -i '/RelNonClosure_MC12/d' $FILE
    sed -i '/Flavor_Comp/d' $FILE
    sed -i '/Flavor_Response/d' $FILE
    sed -i '/BJESUnc/d' $FILE
    sed -i '/Pileup_Mu/d' $FILE
    sed -i '/Pile_NPV/d' $FILE
    

done