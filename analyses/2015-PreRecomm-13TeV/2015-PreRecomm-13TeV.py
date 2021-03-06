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

title = "Pre-recommendations flavor tagging results"
name = "2015-PreRecomm-13TeV"
description = "Flavor tagging pre-recommendations based on 8 TeV and simulation for early Run-II analysis"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

#!! pre-recommendations are based on Run-I results plus extrapolation systematic

# mapping of the Run-I => Run-II working points for the b-jet SFs for calo-jets
# 
# MV1c@60 => MV2c20@60
# MV1c@70 => MV2c20@70
# MV1c@80 => MV2c20@77
# MV1c@80 => MV2c20@85

# mapping of the Run-I => Run-II working points for the c- and light jets SFs for calo-jets
#
# MV1c@50 => MV2c20@60
# MV1c@60 => MV2c20@70
# MV1c@70 => MV2c20@77
# MV1c@80 => MV2c20@85

# mapping of the Run-I => Run-II working points for the track-jets gets tricky as we don't always have Run-I results
#
# b-jet SF
# MV1c@70 => MV2c20@70 (d=0.2)
# MV1c@77 => MV2c20@70 (d=0.3)
#
# c-jet SF
# MV1c@60 => MV2c20@70 (from calo-jet to d=0.2,0.3)
#
# light-jet SF
#

# MC15 working points derived on June 22nd, 2015 and available at BTaggingBenchmarks twiki

taggers = [
# OLD WAY!
#MV2c20 60% (calo-jet)
#    ["MV2c20", "0.4496"],
#MV2c20 70% (calo-jet)
#    ["MV2c20", "-0.0436"],
#MV2c20 77%, (calo-jet)
#    ["MV2c20", "-0.4434"],
#MV2c20 85% (calo-jet)
#    ["MV2c20", "-0.7887"],
# NEW WAY!
#MV2c20 60%
    ["MV2c20", "FixedCutBEff_60"],
#MV2c20 70%
    ["MV2c20", "FixedCutBEff_70"],
#MV2c20 77%
    ["MV2c20", "FixedCutBEff_77"],
#MV2c20 85%
    ["MV2c20", "FixedCutBEff_85"]
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict_good = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4EMTopoJets","AntiKt2PV0TrackJets"],
    ).verify_OPs("13TeV")

sfObject.restrict_ignore = lambda self: self.filter(
    ignore=[".*25-pt-30.*",".*300-pt-400.*"]
    )
	
sfObject.restrict = lambda self: self.restrict_good().restrict_ignore()
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#


ttbar_pdf_7_all = files("ttbar_pdf/EM/JVF05/6PT_MV1c/*6bins.txt") \
                  .restrict() \
                  .filter(analyses = ["PDF_6bins_emu_2j", "PDF_6bins_emu_3j", \
                                      "PDF_6bins_ll_2j", "PDF_6bins_ll_3j", \
                                      ])

ttbar_pdf_7_2j = ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_ll_2j", "PDF_6bins_emu_2j", \
                                     ])

ttbar_pdf_7_3j = ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_ll_3j", "PDF_6bins_emu_3j", \
                                     ])

sources_7  = ttbar_pdf_7_all


# The file "commonbinning.txt" just contains some empty specifications that have the binning. They don't contain
# any real data. It should have the same binning as the D*. The _30 is without the 20-30 to deal with the PDF method,
# which has a bin we ignore from 25-30, and that bin can't really participate.
#

rebin_template_all = files("commonbinning.txt") \
    .filter(analyses=["rebin"])

rebin_template = rebin_template_all \
                 .filter(ignore=[".*300-pt-500.*", ".*500-pt-800.*", ".*800-pt-1200.*", ".*1200-pt-2000.*"])

rebin_template_30 = files("commonbinning.txt") \
                    .filter(analyses=["rebin_30"]) \
                    .filter(ignore=[".*300-pt-500.*", ".*500-pt-800.*", ".*800-pt-1200.*", ".*1200-pt-2000.*"])

#
# We want several versions of the pdf fit to end up in the
# final file. This is for specialized use.
#

ttbar_pdf_7_combined_withchi2 = ttbar_pdf_7_all.bbb_fit("ttbar_PDF_7b", saveCHI2Fits=True)
ttbar_pdf_7_combined = ttbar_pdf_7_combined_withchi2.filter(analyses=["ttbar_PDF_7b"])
ttbar_pdf_7_combined_2j = ttbar_pdf_7_2j.bbb_fit("ttbarPDF7b2j")
ttbar_pdf_7_combined_3j = ttbar_pdf_7_3j.bbb_fit("ttbarPDF7b3j")

# one ring to rule them all...
ttbar_fits_7 = ttbar_pdf_7_combined \
    + ttbar_pdf_7_combined_2j \
    + ttbar_pdf_7_combined_3j

ttbar_fits = ttbar_fits_7

#
# Next, we need to build up the master fits that will be used to make charm and tau results.
# This requires re-binning to match the D* input bins (for both charm and tau, as they
# are just versions of each other).
# Use one of the D* results as the rebin template.
#

dstar_rebin_template = files("Dstar/EM/JVF05/DStar_MV1c70.txt")

ttbar_rebin = (dstar_rebin_template + ttbar_fits) \
              .rebin("DStar", "<>_rebin")


####################################
# Tau and Charm
#

# Calculate the new D* values for charm. Use the algorithm provided by Fabrizio.
# The tau is just an additional error on top of that.
#

dstar_template = files("Dstar/EM/JVF05/*.txt")\
                 .restrict()

charm_sf = (dstar_template + ttbar_rebin) \
           .dstar("DStar_<>", "DStar")
                 
tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources_4 = dstar_template

####################################
# Light SF come from the negative tags
#

negative = files("negative_tags/EM/JVF05/mistag*.txt") \
           .restrict()

light_sf = negative

####################################
# Extrapolate everything
#

mcCalib_bct_all = (files("MCcalib/SfPtB*.txt") + files("MCcalib/SfPtC*.txt") + files("MCcalib/SfPtT*.txt")) \
              .restrict_good()
	
mcCalib_l_all =  files("MCcalib/EtaBins/SfPtL*.txt") \
            .restrict_good()

mcCalib_bct = mcCalib_bct_all \
			  .filter(ignore=[".*15-pt-20.*",".*20-pt-30.*",".*30-pt-40.*",".*40-pt-50.*",".*50-pt-60.*"])

mcCalib_l = mcCalib_l_all \
            .filter(ignore=[".*15-pt-20.*",".*20-pt-30.*",".*30-pt-40.*",".*40-pt-50.*",".*50-pt-60.*",".*60-pt-75.*",".*75-pt-90.*",".*90-pt-110.*",".*110-pt-140.*",".*140-pt-200.*",".*200-pt-300.*"])
			
rebin_template_high = rebin_template_all \
    .filter(ignore=[".*20-pt-30.*"])

mcCalib_rebin_bct = (rebin_template_high + mcCalib_bct) \
    .rebin("rebin", "<>_rebin")

rebin_for_extrap_dstar = files("commonbinning.txt") \
                       .filter(analyses=["rebin_dstar"])

mcCalib_rebin_dstar_bct = (rebin_for_extrap_dstar + mcCalib_bct) \
    .rebin("rebin_dstar", "<>_rebin")

rebin_extrapolated = (\
    mcCalib_rebin_bct
    + ttbar_fits_7 \
    + sources_7 \
    ) \
    .extrapolate("MCcalib_rebin")
	
rebin_dstar_extrapolated = (\
    charm_sf \
    + tau_sf \
    + mcCalib_rebin_dstar_bct \
	) \
	.extrapolate("MCcalib_rebin")

light_extrapolated = (light_sf + mcCalib_l).extrapolate("MCcalib")

all_extrapolated = rebin_extrapolated + rebin_dstar_extrapolated + light_extrapolated

####################################
# Track-jets - b jets
#

ttbar_topo_trackjets = files("ttbar_topo/*.txt") \
                       .restrict_good() \
                       .filter(analyses = ["ttbar_topo_dijet"])

mcCalib_b_trackjets = files("MCcalib/AntiKt*SfPtB*.txt") \
                      .restrict_good() \

b_trackjets_extrap = (ttbar_topo_trackjets + mcCalib_b_trackjets) \
                     .extrapolate("MCcalib")

####################################
# Track-jets - c jets
#

dstar_rebin_template_trackjets = files("commonbinning.txt") \
                                 .filter(analyses=["rebin_dstar_trackjet"])

ttbar_topo_rebin_trackjets = (dstar_rebin_template_trackjets + ttbar_topo_trackjets) \
                             .rebin("rebin_dstar_trackjet", "<>_rebin")

dstar_trackjets = files("Dstar/EM/JVF05/AntiKt*.txt") \
                       .restrict_good()

charm_trackjets = (dstar_trackjets + ttbar_topo_rebin_trackjets) \
                  .dstar("DStar_<>", "DStar")
                 
tau_trackjets = charm_trackjets.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

mcCalib_ct_trackjets = (files("MCcalib/AntiKt*SfPtC*.txt") + files("MCcalib/AntiKt*SfPtT*.txt")) \
                       .restrict_good() \

ct_trackjets_extrap = (charm_trackjets + tau_trackjets + mcCalib_ct_trackjets) \
                       .extrapolate("MCcalib")

####################################
# Track-jets - light jets
#

negative_trackjets = files("negative_tags/EM/JVF05/AntiKt*.txt") \
                     .restrict_good() \
                     .filter(analyses = ["negative_tags"])

mcCalib_l_trackjets = files("MCcalib/EtaBins/AntiKt*.txt") \
                      .restrict_good() \

negative_trackjets_extrap = (negative_trackjets + mcCalib_l_trackjets).extrapolate("MCcalib")


####################################
# Track-jets - altogether
#

sf_trackjets = b_trackjets_extrap + ct_trackjets_extrap + negative_trackjets_extrap

####################################
# The CDI file.
#

master_cdi_file = all_extrapolated+sf_trackjets
defaultSFs = master_cdi_file.make_cdi("MC12-CDI", "defaults.txt","StandardTag-13TeV-prerecommendationCalibrationFile3-151023094730.root","BtagWP-Oct2015.root")
master_cdi_file.plot("MC12-CDI", effOnly=True)
master_cdi_file.dump(linage=True, name="master-cdi-linage")
master_cdi_file.plot("MC12-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
(ttbar_pdf_7_combined_withchi2).plot("MC12-CHi2-Errors")
(sources_7+sources_4).dump(sysErrors = True, name="sources")
(mcCalib_bct_all+mcCalib_l_all).plot("MC12-MCExtrapolations")

# Done!
