#!/bin/env python
#
# Remake the input topo file.
#
#  This version of the script is hard-wired. As we get more experience
# with having to do this we may want to do other things to the
# file.
#

import os
from ROOT import TFile, gSystem
gSystem.Load("libCalibrationDataInterfaceLib")

input_file = "analyses/2012-Summer/TopCalibrations_rel17_MC12a_Convert.root"
output_file = "Convert.root"

#
# Make sure everything exists
#

if not os.path.exists (input_file):
    raise "Can't file file %s" % input_file

#
# Load it up
#

fin = TFile.Open(input_file, "READ")
fout = TFile.Open(output_file, "RECREATE")

#
# Now, do it for each tagger
#

taggers = fin.GetListOfKeys()
for t in taggers:
    print t.GetName()
    tagger_in = t.ReadObj()
    tagger_out = fout.mkdir(tagger_in.GetName())
    for j in tagger_in.GetListOfKeys():
        print "  ", j.GetName()
        jet_in = j.ReadObj()
        for jet_out_name in ["AntiKt4TopoEM", "AntiKt4TopoLC"]:
            jet_out = tagger_out.mkdir(jet_out_name)
            for op in jet_in.GetListOfKeys():
                print "    ", op.GetName()
                op_in = op.ReadObj()
                op_out = jet_out.mkdir(op_in.GetName())
                for f in op_in.GetListOfKeys():
                    print "      ", f.GetName()
                    flavor_in = f.ReadObj()
                    flavor_out = op_out.mkdir(flavor_in.GetName())
                    for h  in flavor_in.GetListOfKeys():
                        print "        ", h.GetName()
                        hist = h.ReadObj()
                        flavor_out.cd()
                        hist.Write()
                
    

#
# Done!
#
fin.Close()
fout.Write()
fout.Close()

