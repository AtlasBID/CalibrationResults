#
# Config for doing the full combination with muon, ttbar, neg tag, and charm
# for the 2012 Paper.
#

title = "Winter 2013 B-Tagging SF Results"
name = "2013-Winter"
description = "Winter 2013 results for dijet and ttbar, based on 2012 data"

#
# Input arguments
#

inputs = [
    "pTRel/*.txt",
    
#    "DStar/*.txt",
#    "system8/*.txt",
#    "sv0mass/*.txt",
#    "negativetag/*.txt",
#    "negativetag/TrigMediumBL1/*.txt",
#    "negativetag/TrigMediumL2M/*.txt",
#    "negativetag/TrigTightBL1/*.txt",
#    "negativetag/TrigTightL2M/*.txt",
#    "KinSel_ljet/*.txt",
#    "KinSel_dilet/*.txt",
    
#    "stat_correlation_inputs.txt",
#    "cc_MV1-test.txt",
#    "defaults.txt",
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
    ["MV1", "0.905363"], 
#    ["MV1", "0.601713"], 
#    ["MV1", "0.404219"],
#    ["MV1", "0.0714225"],
#    ["SV0", "5.65"],
    ]

TrigTagBuilder = [
    ["", "-999"],
    ["JetFitterCOMBNN", "2.20"],
    ["JetFitterCOMBNN", "-1.25"],
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
    'bottom': {
    'dijet': ["pTrel", "system8"],
    },
    }

#
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
    ".*:20-pt-200:.*", 
    ".*:25-pt-30:.*",

    "pTrel-system8-bottom-.*-AntiKt4Topo:200-pt-250:0-abseta-2.5",
    "sv0mass-light-MV1-0.601713-AntiKt4Topo.*",
    "negative.*-light-TrigTight_JetFitterCOMBNN_.*-0.35-AntiKt4Topo:.*",
    "negative.*-light-TrigMedium_JetFitterCOMBNN_.*-0.35-AntiKt4Topo:.*",
    "negative.*-light-TrigTight_JetFitterCOMBNN_.*-1.80-AntiKt4Topo:.*",
    "negative.*-light-TrigMedium_JetFitterCOMBNN_.*-1.80-AntiKt4Topo:.*",
    ]

#
# The root file that we start everything with.
#

mcEffRootFile = "TopCalibrations_rel17.2.4_MC12c.root.root"
CDIFile = "%s-rel17.2.4_MC12c.root" % name

#
# Should we avoid the combination?
#

runCombination = True