#
# This file runs the fitting for the b-tag combination. Uses a slightly functional syntax to track files
# throught the system.
#
# We run on the 2012 Paper results, building up lots for show and tell.
#

from files import files
from sfObject import sfObject

title = "Paper 2012 B-Tagging SF Results"
name = "2012-Paper-new"
description = "Final 2011 results for dijet and ttbar, for the b-tagging paper"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

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

ignore_analyses = [
    "pTrel-.*20-pt-200", 
    ".*:25-pt-30:.*",
	
# We have ttbar_pdf for some of the points, so we want to use these instead
# of the ones from the kinematic selection (there are overlap problems there).

	"ttbar_kinsel.*-MV1-0.601713.*",
	"ttbar_kinsel.*-MV1-0.164.*",
	"ttbarKFlepjet.*-MV1-0.601713.*",
	"ttbarKFlepjet.*-MV1-0.164.*",

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
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict = lambda self: self.filter(
    taggers=taggers,
    ignore=ignore_analyses
    )
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#

s8 = files("system8/*.txt") \
     .restrict()
     
ptrel = files("ptrel/*.txt") \
    .restrict()
	
ttbar_pdf_7_all = files ("ttbar_pdf/6bin/*.txt") \
                    .restrict()

ttbar_pdf_10_all = files("ttbar_pdf/9bin/*.txt") \
                   .restrict()
				   
ttbar_kinfit = files("KinFit_ljet/*.txt") \
					.restrict()
					
ttbar_kinsel = files("KinSel_dilet/*.txt") \
					.restrict()

#
# Fit PDF results, with a mind to showing compatibility, etc.
#
                 
ttbar_pdf_7_combined_extra = ttbar_pdf_7_all.bbb_fit("PDF_ll_7_fit", saveCHI2Fits=True)
ttbar_pdf_10_combined_extra = ttbar_pdf_10_all.bbb_fit("PDF_ll_10_fit", saveCHI2Fits=True)
ttbar = ttbar_pdf_10_combined_extra.filter(analyses=["PDF_ll_10_fit"])

#
# And the dijet as well
#

dijet_r = (s8 + ptrel).bbb_fit("dijet", saveCHI2Fits=True, extraFiles=files("stat_correlation_inputs.txt"))
dijet = dijet_r.filter(analyses=["dijet"])

#
# The old ttbar
#

ttbar_paper_r = (ttbar_kinfit+ttbar_kinsel).bbb_fit("ttbar", saveCHI2Fits=True)
ttbar_paper = ttbar_paper_r.filter(analyses=["ttbar"])

#
# And combine them totally
#

all_r = (dijet+ttbar).bbb_fit("all", saveCHI2Fits=True)
all = all_r.filter(analyses=["dijet","PDF_ll_10_fit","all"])

all_paper_r = (s8+ptrel+ttbar_kinfit+ttbar_kinsel).bbb_fit("all_paper", saveCHI2Fits=True)
all_paper = all_paper_r.filter(analyses=["all_paper"])

#
# Now the negative tags
#

light = (files("negativetag/*.txt") + files("sv0mass/*.txt")) \
	    .restrict()
	
#
# Charm and tau
#

charmtau = files("DStar/*.txt") \
		   .restrict()

####
# CDI
(dijet+ttbar+all+light+charmtau).make_cdi("rel17_MC11b-CDI", "defaults.txt", "TopCalibrations_rel17_MC11b_Convert.root")

####################################
# Plotting

#(ttbar_pdf_7_all + ttbar_pdf_7_combined_extra).plot("ttbar_pdf_7", effOnly=True)
#(ttbar_pdf_10_all + ttbar_pdf_10_combined_extra).plot("ttbar_pdf_10", effOnly=True)
#(ttbar_kinfit+ttbar_kinsel+ttbar_paper_r).plot("ttbar_paper", effOnly=True)
#(s8+ptrel+ttbar_kinfit+ttbar_kinsel+all_paper_r).plot("all_paper", effOnly=True)
#(s8+ptrel+dijet_r).plot("dijet", effOnly=True)
#(dijet+ttbar+all).plot("all", effOnly=True)
#(dijet+ttbar+all).plot("all_perTagger", effOnly=True, byTaggerEff=True)
