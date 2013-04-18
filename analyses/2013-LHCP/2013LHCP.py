#
# Config for doing the full combination with muon, ttbar, neg tag, and charm
# for the 2012 Paper.
#

title = "Spring 2013 B-Tagging SF Results - LHCP"
name = "2013-LHCP"
description = "Spring 2013 results, based on the full 2012 data, for LHCP"

#
# Input arguments
#

inputs = [
#    "system8/*.txt",
#    "pdfmethod_ttdilep/*.txt",
    "topo_ttemu/*.txt",

#   "pTRel/*.txt",
#    "DStar/*.txt",
#    "negativetag/*.txt",
    
#    "defaults.txt",

#    "sv0mass/*.txt",
#    "negativetag/TrigMediumBL1/*.txt",
#    "negativetag/TrigMediumL2M/*.txt",
#    "negativetag/TrigTightBL1/*.txt",
#    "negativetag/TrigTightL2M/*.txt",
#    "KinSel_ljet/*.txt",
#    "KinSel_dilet/*.txt",
    
#    "stat_correlation_inputs.txt",
#    "cc_MV1-test.txt",
#    "trigger_config.txt"
    ]

taggers = [
#    ["IP3DSV1", "4.55"],
#    ["IP3DSV1", "1.70"],
#    ["IP3DSV1", "-0.80"],
#    ["JetFitterCOMBNN", "2.20"],
#    ["JetFitterCOMBNN", "1.80"],
#    ["JetFitterCOMBNN", "0.35"],
#    ["JetFitterCOMBNN", "-1.25"],
#    ["JetFitterCOMBNNc", "1.33"],
#    ["JetFitterCOMBNNc", "0.98"],

#MV1 60% JVF (EM, LC), noJVF (EM, LC)
    ["MV1", "0.9867"], 
    ["MV1", "0.9827 "], 
#MV1 70%
    ["MV1", "0.8119"], 
    ["MV1", "0.7892"], 
#MV1 80%
    ["MV1", "0.3900"], 
    ["MV1", "0.3511"], 
#MV1c 50% JVF (EM, LC)
    ["MV1c", "0.9237"], 
    ["MV1c", "0.9195"], 
#MV1c 57% JVF (EM, LC)
    ["MV1c", "0.8674"], 
    ["MV1c", "0.8641"], 
	
    ]

TrigTagBuilder = [
#    ["", "-999"],
#    ["JetFitterCOMBNN", "2.20"],
#    ["JetFitterCOMBNN", "-1.25"],
    ]

TrigTagDataInfo = [
#    "TrigTight%s_BE",
#    "TrigTight%s_KL1",
#    "TrigTight%s_L2M",
#    "TrigMedium%s_BE",
#    "TrigMedium%s_KL1",
#    "TrigMedium%s_L2M",
    ]

for tt in TrigTagDataInfo:
    for tbld in TrigTagBuilder:
        tname = tbld[0]
        if len(tname) != 0:
            tname = "_%s" % tname
        s = [tt % tname, tbld[1]]
        taggers.append(s)

DoOnlyTaggers = []

for t in taggers:
    d = {
        "flavor":"*",
        "tagger":t[0],
        "op":t[1],
        "jet":"*"
        }
    DoOnlyTaggers.append(d)
    
#
# Analysis Groupings - how we want the combination to run
#

analysisGroupings = {
    }

#
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
# These are extra bins put in by ptrel, which we don't
# want to use in a fit.
    ".*:20-pt-200:.*", 

# Some ttbar analyses start funny, but all bins must match, so
# we have to ignore the half bins.
    ".*:25-pt-30:.*",

# There are a number of OPs that are in the calibration files that shouldn't be in the
# calibration files.
    ]

#
# The root file that we start everything with.
#

mcEffRootFile = "TopCalibrations_rel17.2.1.4_MC12.root"
CDIFile = "%s-rel17.2.1.4_MC12-LHCP.root" % name

#
# Should we avoid the combination?
#

runCombination = True
