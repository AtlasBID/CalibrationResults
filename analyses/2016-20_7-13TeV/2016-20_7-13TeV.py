#
# This file runs the fitting for the b-tag combination. Uses a slightly functional syntax to track files
# through out the system.
#
# The system is intelligent about how it deals with file dates - so it won't re-run if the inputs are older than the
# outputs. However, it doesn't currently detect when an executable has been updated - so it will fail to run in those
# circumstances.
#

#
# Important imports to get things off the ground.
#

from files import files
from sfObject import sfObject

title = "Recommendations of flavor tagging results for 13 TeV collisions on 20.7 release"
name = "2016-20_7-13TeV"
description = "Flavor tagging recommendations based on 13 TeV and simulation for the 2016 Run-II analysis on 20.7 release"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

# Master file for the recommendations on release 20.7 
# we start with just the definition of the working
# points and the efficiency maps for the MV2c10 and MV2c20

taggers = [
#MV2c20 60%
    ["MV2c20", "FixedCutBEff_60"],
    ["MV2c20", "FlatBEff_60"],
#MV2c20 70%
    ["MV2c20", "FixedCutBEff_70"],
    ["MV2c20", "FlatBEff_70"],
#MV2c20 77%
    ["MV2c20", "FixedCutBEff_77"],
    ["MV2c20", "FlatBEff_77"],
##MV2c20 85%
    ["MV2c20", "FixedCutBEff_85"],
    ["MV2c20", "FlatBEff_85"],
##MV2c10 60%
    ["MV2c10", "FixedCutBEff_60"],
    ["MV2c10", "FlatBEff_60"],
#MV2c10 70%
    ["MV2c10", "FixedCutBEff_70"],
    ["MV2c10", "FlatBEff_70"],
#MV2c10 77%
    ["MV2c10", "FixedCutBEff_77"],
    ["MV2c10", "FlatBEff_77"],
#MV2c10 85%
    ["MV2c10", "FixedCutBEff_85"],
    ["MV2c10", "FlatBEff_85"]
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict_good = lambda self: self.filter(
    taggers=taggers,
    #jets=["AntiKt4EMTopoJets","AntiKt2PV0TrackJets","AntiKt4PV0TrackJets"],
    # initial hack to exclude any calibration from a CDI file
    jets=["AntiKtEMTopoJets"],
    ).verify_OPs("13TeV")

sfObject.restrict_ignore = lambda self: self.filter(
    ignore=[".*25-pt-30.*",".*300-pt-400.*"]
    )

sfObject.restrict_ignore_tight = lambda self: self.filter(
    ignore=[".*25-pt-30.*",".*200-pt-300.*",".*250-pt-300.*",".*300-pt-400.*"]
    )

sfObject.restrict = lambda self: self.restrict_good().restrict_ignore()

sfObject.restrict_tight = lambda self: self.restrict_good().restrict_ignore_tight()

	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#

# Run-I PDF pre-recommendations
pre_ttbar_pdf_7_all = files("../2016-Winter-13TeV/ttbar_pdf/pre/*6bins.txt") \
                  .restrict() \
                  .filter(analyses = ["pre_PDF_6bins_emu_2j", "pre_PDF_6bins_emu_3j", \
                                      "pre_PDF_6bins_ll_2j", "pre_PDF_6bins_ll_3j"])

sources_ttbar  = pre_ttbar_pdf_7_all

####################################
# The CDI file.
#

master_cdi_file = sources_ttbar
defaultSFs = master_cdi_file.make_cdi("MC15-CDI", "defaults.txt","ToMerge_AntiKt4EMTopoJets_20160505.root","ToMerge_StandardTag-13TeV-release20.7-160511140113.root")
master_cdi_file.plot("MC15-CDI", effOnly=True)
master_cdi_file.dump(linage=True, name="master-cdi-linage")
master_cdi_file.plot("MC15-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")

# Done!
