#
# Config for doing the MV180 combination and file generation for dijets only.
#

title = "Winter 2012 B-Tagging SF Results"
name = "2012-Winter"

#
# Input arguments
#

inputs = [
    "analyses/2012-Winter/DStar/*.txt",
    "analyses/2012-Winter/system8/*.txt",
    #"/Projects/notes/Winter2012/negativetagsCOM/tables/NegativeTagCombine/uncorr/*.txt",
    #"/Projects/notes/Winter2012/sv0massCOM/files/uncorr/*.txt",
    #"/Projects/notes/Winter2012/negativetagsCOM/tables/NegativeTagCombine/binbybin/*.txt",
    #"/Projects/notes/Winter2012/sv0massCOM/files/binbybin/*.txt",
    "analyses/2012-Winter/sv0mass/*.txt",
    "analyses/2012-Winter/negativetag/*.txt",
    "analyses/2012-Winter/negativetag/TrigMediumBL1/*.txt",
    "analyses/2012-Winter/negativetag/TrigMediumL2M/*.txt",
    "analyses/2012-Winter/negativetag/TrigTightBL1/*.txt",
    "analyses/2012-Winter/negativetag/TrigTightL2M/*.txt",

    "analyses/2012-Winter/ptrel/*.txt",
    "analyses/2012-Winter/stat_correlation_inputs.txt",
    "analyses/2012-Winter/defaults.txt",
    "analyses/2012-Winter/trigger_config.txt"
    ]

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
    "TrigTight%s_BE",
    "TrigTight%s_KL1",
    "TrigTight%s_L2M",
    "TrigMedium%s_BE",
    "TrigMedium%s_KL1",
    "TrigMedium%s_L2M",
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
    "pTrel-bottom-.*-AntiKt4Topo:20-pt-200:0-abseta-0.6", 
    "pTrel-bottom-.*-AntiKt4Topo:20-pt-200:0.6-abseta-1.2",
    "pTrel-bottom-.*-AntiKt4Topo:20-pt-200:1.2-abseta-1.8",
    "pTrel-bottom-.*-AntiKt4Topo:20-pt-200:1.8-abseta-2.5",
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

mcEffRootFile = "mceff/TopCalibrations_rel17_MC11b_Convert.root"
CDIFile = "%s-rel17_MC11b.root" % name

#
# Should we avoid the combination?
#
runCombination = True
