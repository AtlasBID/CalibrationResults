#
# Config for doing the full combination with muon, ttbar, neg tag, and charm
# for the 2012 Paper.
#

title = "Paper 2012 B-Tagging SF Results Without Semileptonic Sys Error"
name = "2012-Paper-NoSemiLeptonic"
description = "Final 2011 results for dijet and ttbar, for the b-tagging paper. The dijet semi-leptonic to inclusive systematic error has been dropped."

#
# Input arguments
#

inputs = [
    "DStar/*.txt",
    "system8/*.txt",
    "sv0mass/*.txt",
    "negativetag/*.txt",
    "negativetag/TrigMediumBL1/*.txt",
    "negativetag/TrigMediumL2M/*.txt",
    "negativetag/TrigTightBL1/*.txt",
    "negativetag/TrigTightL2M/*.txt",
    "ptrel/*.txt",
    "KinFit_ljet/*.txt",
    "KinSel_dilet/*.txt",

    "stat_correlation_inputs.txt",
    "defaults.txt",
    "trigger_config.txt"
    ]
    
droppedSystematicErrors = ["scale factor for inclusive b-jets"]

taggers = [
    ["IP3DSV1", "4.55"],
    ["IP3DSV1", "1.70"],
    ["IP3DSV1", "-0.80"],
    ["JetFitterCOMBNN", "2.20"],
    ["JetFitterCOMBNN", "1.80"],
    ["JetFitterCOMBNN", "0.35"],
    ["JetFitterCOMBNN", "-1.25"],
    ["JetFitterCOMBNNc", "1.33"],
    ["JetFitterCOMBNNc", "0.98"],
    ["MV1", "0.905363"], 
    ["MV1", "0.601713"], 
    ["MV1", "0.404219"],
    ["MV1", "0.0714225"],
    ["SV0", "5.65"],
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
		'ttbar': ["ttbarKFlepjet", "ttbar_kinsel_dilep"],
		'all': ["ttbarKFlepjet", "ttbar_kinsel_dilep", "pTrel", "system8"],
		},
	'light': {},
	'charm': {},
	'tau': {}
    }

CombinationTypeInfo = [
    { "type": "binbybin", "prefix" : "bbb_" },
    { "type": "profile", "prefix" : "" }
    ]

#
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
    "pTrel-.*-AntiKt4Topo:20-pt-200:0-abseta-0.6", 
    "pTrel-.*-AntiKt4Topo:20-pt-200:0.6-abseta-1.2",
    "pTrel-.*-AntiKt4Topo:20-pt-200:1.2-abseta-1.8",
    "pTrel-.*-AntiKt4Topo:20-pt-200:1.8-abseta-2.5",

    ".*:25-pt-30:.*",
	
# left over from some folks adding stuff that shouldn't be in here.
	".*JetProb.*",
	".*IP3DSV1-1.55.*",
	".*SV060-1e-06.*",

# Some other things that should be left out because it was easy to put the files
# in.

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

mcEffRootFile = "TopCalibrations_rel17_MC11b_Convert.root"
CDIFile = "%s-rel17_MC11b.root" % name

#
# Should we avoid the combination?
#

runCombination = True
