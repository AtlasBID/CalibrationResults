#
# This is the 2012 Data HCP version
#  - Use MC12 MC Eff
#  - Use ptrel from 2012 data run
#  - Use neg tags from 2012 data run
#  - Use ttbar results from 2011 run (not ready yet)
#

title = "2012 full dataset B-Tagging SF Results"
description = "Uses HCP 2012 results for all but ttbar inputs. ttbar calibration results are from 2011, the full run."
name = "2012-Fall-MC12Data"

#
# Input arguments
#

inputs = [
    "DStar/*.txt",
    "negativetag/*.txt",

    "ptrel/*.txt",

    "KinFit_ljet/*.txt",
    "KinSel_ljet/*.txt",
    "KinSel_dilet/*.txt",

    "defaults.txt",
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
# Optional analysis groupings. This is used if more than one
# grouping of combination is desired. The results are all put in the
# same final file, of course. If a flavor entry is missing, then everything
# for that flavor is done. Otherwise, *only* what is listed is done. The empty
# [], btw, means everything should be done.
#

analysisGroupings = {
    'bottom': {
      'all': [],
      'dijet': ["pTrel", "system8"],
      'ttbar': ["ttbar_kinsel_dilep", "ttbar_kinsel_ljet"],
      }
}

#
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
    "pTrel-.*-AntiKt4Topo:20-pt-200:0-abseta-0.6", 
    "pTrel-.*-AntiKt4Topo:20-pt-200:0.6-abseta-1.2",
    "pTrel-.*-AntiKt4Topo:20-pt-200:1.2-abseta-1.8",
    "pTrel-.*-AntiKt4Topo:20-pt-200:1.8-abseta-2.5",

    # Drop the first bin in the ttbar
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

mcEffRootFile = "TopCalibrations_rel17_MC11b_Convert.root"
CDIFile = "%s-rel17_MC12a_DJ12a_tt11.root" % name

#
# Should we avoid the combination?
#

runCombination = True
