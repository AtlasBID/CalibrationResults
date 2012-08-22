#
# Config for doing the MV180 combination and file generation for dijets only.
#

title = "Summer 2012 NoJVF B-Tagging SF Results"
name = "2012-SummerNoJVF"

#
# Input arguments
#

inputs = [
    "DStar/noJVF/*.txt",
    #"system8/*.txt",
    #"sv0mass/*.txt",
    "negativetag/noJVF/*.txt",
    #"negativetag/TrigMediumBL1/*.txt",
    #"negativetag/TrigMediumL2M/*.txt",
    #"negativetag/TrigTightBL1/*.txt",
    #"negativetag/TrigTightL2M/*.txt",
    "ptrel/noJVF/*.txt",

    #"stat_correlation_inputs.txt",
    "defaults.txt",
    #"trigger_config.txt"
    ]

taggers = [
    ["JetFitterCOMBNN", "1.10"],
    ["JetFitterCOMBNN", "0.65"],
    ["JetFitterCOMBNN", "-0.95"],
    ["JetFitterCOMBNN", "-2.60"],

    ["JetFitterCOMBNN", "1.00"],
    ["JetFitterCOMBNN", "0.55"],
    ["JetFitterCOMBNN", "-2.55"],

    ["JetFitterCOMBNNc", "1.05"],
    ["JetFitterCOMBNNc", "1.00"],
    ["JetFitterCOMBNNc", "0.50"],
    ["JetFitterCOMBNNc", "0.45"],

    ["MV1", "0.985"], 
    ["MV1", "0.795"], 
    ["MV1", "0.596"],
    ["MV1", "0.148"],

    ["MV1", "0.980"], 
    ["MV1", "0.772"], 
    ["MV1", "0.595"],
    ["MV1", "0.122"],

    ["SV0", "5.70"],
    ["SV0", "5.65"],
    ]

TrigTagBuilder = [
    ]

TrigTagDataInfo = [
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
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
    "pTrel-.*-AntiKt4Topo.*:20-pt-200:0-abseta-0.6", 
    "pTrel-.*-AntiKt4Topo.*:20-pt-200:0.6-abseta-1.2",
    "pTrel-.*-AntiKt4Topo.*:20-pt-200:1.2-abseta-1.8",
    "pTrel-.*-AntiKt4Topo.*:20-pt-200:1.8-abseta-2.5",

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

#mcEffRootFile = "TopCalibrations_rel17_MC12a_Convert.root"
mcEffRootFile = "Convert.root"
CDIFile = "%s-rel17_MC12a.root" % name

#
# Should we avoid the combination?
#

runCombination = True
