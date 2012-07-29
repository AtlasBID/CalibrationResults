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
# The copies we want to make
#

copies = {
    ("SV0", "AntiKt4Topo_EM", "5_70") : (("SV0", "AntiKt4TopoEM", "5_70"), ("SV0", "AntiKt4TopoLC", "5_65")),
    ("JetFitterCOMBNN", "AntiKt4Topo_EM", "1_10") : (("JetFitterCOMBNN", "AntiKt4TopoEM", "1_10"), ("JetFitterCOMBNN", "AntiKt4TopoLC", "1_00")),
    ("JetFitterCOMBNN", "AntiKt4Topo_EM", "0_65") : (("JetFitterCOMBNN", "AntiKt4TopoEM", "0_65"), ("JetFitterCOMBNN", "AntiKt4TopoLC", "0_55")),
    ("JetFitterCOMBNN", "AntiKt4Topo_EM", "-0_95") : (("JetFitterCOMBNN", "AntiKt4TopoEM", "-0_95"), ("JetFitterCOMBNN", "AntiKt4TopoLC", "-0_95")),
    ("JetFitterCOMBNN", "AntiKt4Topo_EM", "-2_60") : (("JetFitterCOMBNN", "AntiKt4TopoEM", "-2_60"), ("JetFitterCOMBNN", "AntiKt4TopoLC", "-2_55")),
    ("MV1", "AntiKt4Topo_EM", "0_985") : (("MV1", "AntiKt4TopoEM", "0_985"), ("MV1", "AntiKt4TopoLC", "0_980")),
    ("MV1", "AntiKt4Topo_EM", "0_795") : (("MV1", "AntiKt4TopoEM", "0_795"), ("MV1", "AntiKt4TopoLC", "0_772")),
    ("MV1", "AntiKt4Topo_EM", "0_596") : (("MV1", "AntiKt4TopoEM", "0_596"), ("MV1", "AntiKt4TopoLC", "0_595")),
    ("MV1", "AntiKt4Topo_EM", "0_148") : (("MV1", "AntiKt4TopoEM", "0_148"), ("MV1", "AntiKt4TopoLC", "0_122")),
    }

#
# A helper function or two
#
def getOrMkdir (dir, name):
    dirName = dir.Get(name)
    if dirName:
        return dirName
    return dir.mkdir(name)

#
# Now, do it for each tagger
#

taggers = fin.GetListOfKeys()
for t in taggers:
    print t.GetName()
    tagger_in = t.ReadObj()
    for j in tagger_in.GetListOfKeys():
        print "  ", j.GetName()
        jet_in = j.ReadObj()
        for op in jet_in.GetListOfKeys():
            print "    ", op.GetName()
            op_in = op.ReadObj()

            #
            # Now, see if there is a match that we are supposed to copy!
            #

            slist = (tagger_in.GetName(), jet_in.GetName(), op_in.GetName())
            tocopy = (slist,)
            if slist in copies:
                tocopy = copies[slist]

            for copySpec in tocopy:
                (tagger_out_name, jet_out_name, op_out_name) = copySpec
                tagger_out = getOrMkdir(fout, tagger_out_name)
                jet_out = getOrMkdir(tagger_out, jet_out_name)
                op_out = getOrMkdir(jet_out, op_out_name)
                
                #
                # And copy over the flavors, etc.
                #

                for f in op_in.GetListOfKeys():
                    print "      ", f.GetName()
                    flavor_in = f.ReadObj()
                    flavor_out = op_out.mkdir(flavor_in.GetName())
                    for h  in flavor_in.GetListOfKeys():
                        print "        ", h.GetName()
                        hist = h.ReadObj()
                        print "          ", hist.GetName(), hist.IsA().GetName()
                        flavor_out.Add(hist)
                
    

#
# Done!
#
fout.Write()
fout.Close()
fin.Close()

