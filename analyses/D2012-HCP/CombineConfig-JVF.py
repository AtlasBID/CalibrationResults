#
# Config for doing the MV180 combination and file generation for dijets only.
#

title = "2012 dataset JVF B-Tagging SF Results"
description = "Uses HCP 2012 ptRel inputs. Uses early 2012 DStar and negative tag results."
name = "D2012-HCP-JVF"

#
# Input arguments
#

inputs = [
    "ptrel/JVF/*.txt",
    "DStar/JVF/*EM.txt",
    "negativetag/JVF/*topoEM_v3.txt",

    "defaults.txt",
    ]

taggersEM = [
    ["MV1", "0.985"], 
    ["MV1", "0.795"], 
    ["MV1", "0.596"], 
    ["MV1", "0.148"], 
    ]

taggersLC = [
    ["MV1", "0.980"], 
    ["MV1", "0.772"], 
    ["MV1", "0.595"], 
    ["MV1", "0.122"], 
    ]

DoOnlyTaggers = []
for t in taggersEM:
    d = {
        "flavor":"*",
        "tagger":t[0],
        "op":t[1],
        "jet":"AntiKt4TopoEM"
        }
    DoOnlyTaggers.append(d)

for t in taggersLC:
    d = {
        "flavor":"*",
        "tagger":t[0],
        "op":t[1],
        "jet":"AntiKt4TopoLC"
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
    }

#
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
    # Drop the first bin in the ttbar
    ".*:25-pt-30:.*",

    # Drop the extra bins in the pTrel analysis
    "pTrel-.*20-pt-200.*",

    # Drop anything to do with the MV2 tagger
    ".*MV2.*",

    ]

#
# The root file that we start everything with.
#

mcEffRootFile = "TopCalibrations_rel17_MC12a_EM_Eff_jvfCut_Convert.root"
CDIFile = "%s-rel17_MC12a_D2012_HCP.root" % name

#
# Should we avoid the combination?
#

runCombination = True
