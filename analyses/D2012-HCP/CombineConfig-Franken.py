#
# Config for doing the MV180 combination and file generation for dijets only.
#

title = "2012 dataset Frankenstine B-Tagging SF Results"
description = "Uses full 2011 5 fb-1 results ttbar results. Uses HCP 2012 ptRel inputs. Uses early 2012 DStar and negative tag results."
name = "D2012-HCP-Frankenstein"

#
# Input arguments
#

inputs = [
    "ptrel/JVF/*.txt",
    "DStar/JVF/*EM.txt",
    "negativetag/JVF/*topoEM_v3.txt",

    "ttbar_ksdlkflj_2011/MV1_70.txt",

    "defaults.txt",
    ]

taggers = [
    ["MV1", "0.795"], 
    ]

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
    'all': ["ttbar_ksdlkflj", "pTrel"]
    }
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

    ]

#
# The root file that we start everything with.
#

mcEffRootFile = "TopCalibrations_rel17_MC12a_EM_Eff_jvfCut_Convert.root"
CDIFile = "%s-rel17_MC12b_D2012_HCP_MV170ONLY.root" % name

#
# Should we avoid the combination?
#

runCombination = True
