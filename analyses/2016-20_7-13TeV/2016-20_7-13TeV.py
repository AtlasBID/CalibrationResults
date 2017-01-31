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

title = "Recommendations of flavor tagging results for 13 TeV collisions"
name = "2016-20_7-13TeV"
description = "Flavor tagging recommendations based on 13 TeV and simulation for the 2016 Run-II analysis"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

# MC15 working points derived on May 2nd, 2016 and available at BTaggingBenchmarks twiki

taggers = [
#MV2c10 60%
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
    ["MV2c10", "FlatBEff_85"],
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict_good = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4EMTopoJets","AntiKt2PV0TrackJets","AntiKt4PV0TrackJets"],
    ).verify_OPs("20_7")

sfObject.restrict_ignore = lambda self: self.filter(
    ignore=[".*25-pt-30.*"]
    )

sfObject.restrict_ignore_tight = lambda self: self.filter(
    ignore=[".*25-pt-30.*",".*200-pt-300.*",".*250-pt-300.*",".*300-pt-400.*"]
    )

sfObject.restrict_ignore_trackjets = lambda self: self.filter(
    ignore=[".*250-pt-300.*"]
    )

sfObject.restrict = lambda self: self.restrict_good().restrict_ignore()

sfObject.restrict_tight = lambda self: self.restrict_good().restrict_ignore_tight()

sfObject.restrict_trackjets = lambda self: self.restrict_good().restrict_ignore_trackjets()
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#

# Run-I PDF pre-recommendations
# these are needed for the c-jet calibration since
# we want the high-pT extrapolation to kick in at 200 GeV
# for the b-jet calibration
pre_ttbar_pdf_7_all = files("bjets/ttbar_pdf/pre/*6bins.txt") \
                  .restrict() \
                  .filter(analyses = ["pre_PDF_6bins_emu_2j", "pre_PDF_6bins_emu_3j", \
                                      "pre_PDF_6bins_ll_2j",  "pre_PDF_6bins_ll_3j"])

# Run-II PDF recommendations
ttbar_pdf_7_all = (files("bjets/ttbar_pdf/*emu*7bins*.txt") + files("bjets/ttbar_pdf/*ll*7bins*.txt")) \
                  .restrict() \
                  .filter(analyses = ["PDF_6bins_emu_2j", "PDF_6bins_emu_3j", \
                                      "PDF_6bins_ll_2j",  "PDF_6bins_ll_3j"]) \
                  .filter(jets=["AntiKt4EMTopoJets"])

ttbar_pdf_7_2j = ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_emu_2j", "PDF_6bins_ll_2j"])

ttbar_pdf_7_3j = ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_emu_3j", "PDF_6bins_ll_3j"])

# Run-II T&P recommendations
ttbar_tp_all = files("bjets/ttbar_topo/TandP*WP.txt") \
                 .restrict_tight() \
                 .filter(analyses = ["TandP_6bins_emu_2jmva","TandP_6bins_emu_3j"])

ttbar_tp_2j = ttbar_tp_all \
                 .filter(analyses = ["TandP_6bins_emu_2jmva"])

ttbar_tp_3j = ttbar_tp_all \
                .filter(analyses = ["TandP_6bins_emu_3j"])

sources_ttbar = ttbar_pdf_7_all + ttbar_tp_all

#
# We want several versions of the pdf fit to end up in the
# final file. This is for specialized use.
#

ttbar_tp_combined_withchi2 = ttbar_tp_all.bbb_fit("ttbar_tp_2j3j", saveCHI2Fits=True)
ttbar_tp_combined = ttbar_tp_combined_withchi2.filter(analyses=["ttbar_tp_2j3j"])
ttbar_tp_combined_2j = ttbar_tp_2j.bbb_fit("ttbar_tp_2j")
ttbar_tp_combined_3j = ttbar_tp_3j.bbb_fit("ttbar_tp_3j")

pre_ttbar_pdf_7_combined_withchi2 = pre_ttbar_pdf_7_all.bbb_fit("pre_ttbar_PDF_7b", saveCHI2Fits=True)
pre_ttbar_pdf_7_combined = pre_ttbar_pdf_7_combined_withchi2.filter(analyses=["pre_ttbar_PDF_7b"])

ttbar_pdf_7_combined_withchi2 = (ttbar_pdf_7_all).bbb_fit("ttbar_PDF_7b", saveCHI2Fits=True)
ttbar_pdf_7_combined = ttbar_pdf_7_combined_withchi2.filter(analyses=["ttbar_PDF_7b"])
ttbar_pdf_7_combined_2j = ttbar_pdf_7_2j.bbb_fit("ttbar_PDF_7b_2j")
ttbar_pdf_7_combined_3j = ttbar_pdf_7_3j.bbb_fit("ttbar_PDF_7b_3j")

# one ring to rule them all...
ttbar_pdf_fits = ttbar_pdf_7_combined \
    + ttbar_pdf_7_combined_2j \
    + ttbar_pdf_7_combined_3j

ttbar_tp_fits = ttbar_tp_combined \
    + ttbar_tp_combined_2j \
    + ttbar_tp_combined_3j

ttbar_fits = ttbar_pdf_fits + ttbar_tp_fits

# Run-II pT-rel recommendations
pTrel = files("bjets/pT_rel/MV2c10*.txt") \
              .filter(analyses = ["pTrel"])

mcCalib_b_all = files("extrap/MCcalibCDI_Zprimebb5000_b*.txt") \
                .restrict()

ttbar_extrapolated = (mcCalib_b_all \
                      + ttbar_fits ) \
                      .extrapolate("Run2MCcalib")

####################################
# Tau and Charm
#

#
# W+c calibration doesn't require the special treatment reserved for D*
#

wc_sf = files("cjets/Wc/W*.txt") \
              .restrict()

tau_sf = wc_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

mcCalib_ct_all = files("extrap/MCcalibCDI_ttbar_c*") + files("extrap/MCcalibCDI_ttbar_t*") \
                .restrict()

charm_sf_extrapolated = (mcCalib_ct_all + wc_sf) \
                     .extrapolate("Run2MCcalib")

tau_sf_extrapolated = (mcCalib_ct_all + tau_sf) \
                     .extrapolate("Run2MCcalib")

sources_wc = wc_sf

####################################
# Light SF come from the negative tags
#

light_sf = files("ljets/negative_tags/negtag*.txt") \
           .restrict()

negative_pre = files("ljets/negative_tags/pre/mistag*.txt") \
           .restrict()

mcCalib_l_pre = files("MCcalib/EtaBins/SfPtL*.txt") \
                .restrict_good() \
                .filter(ignore=[".*15-pt-20.*",".*20-pt-30.*",".*30-pt-40.*",".*40-pt-50.*",".*50-pt-60.*",".*60-pt-75.*",".*75-pt-90.*",".*90-pt-110.*",".*110-pt-140.*",".*140-pt-200.*",".*200-pt-300.*"])

light_sf_pre = (negative_pre + mcCalib_l_pre).extrapolate("MCcalib")

####################################
# Calo-jets - all together
#

all_calojets_extrapolated = ttbar_extrapolated + pTrel \
                            + charm_sf_extrapolated + tau_sf_extrapolated \
                            + light_sf_pre + light_sf

####################################
# Track-jets pre-recommendations - b jets
#

ttbar_pre_r02_trackjets = files("bjets/ttbar_topo/pre/*.txt") \
                       .restrict_good() \
                       .filter(analyses = ["pre_ttbar_topo_dijet"]) \
                       .filter(jets=["AntiKt2PV0TrackJets"])

ttbar_r02_trackjets = (files("bjets/ttbar_pdf/*tracks*emu*.txt") + files("bjets/ttbar_pdf/*tracks*ll*.txt")) \
                       .restrict_trackjets() \
                       .filter(analyses = ["PDF_6bins_emu_2j","PDF_6bins_emu_3j", \
                                           "PDF_6bins_ll_2j", "PDF_6bins_ll_3j"]) \
                       .filter(jets=["AntiKt2PV0TrackJets"])

ttbar_pre_r04_trackjets = files("bjets/ttbar_topo/pre/*.txt") \
                       .restrict_good() \
                       .filter(analyses = ["pre_ttbar_topo_dijet"]) \
                       .filter(jets=["AntiKt4PV0TrackJets"])

ttbar_r04_trackjets = files("bjets/ttbar_pdf/*tracks*.txt") \
                       .restrict_trackjets() \
                       .filter(analyses = ["PDF_6bins_emu_2j","PDF_6bins_emu_3j"]) \
                       .filter(jets=["AntiKt4PV0TrackJets"])

#mcCalib_b_trackjets = files("extrap/AntiKt*Zprimebb*b*.txt") \
mcCalib_b_trackjets = files("MCcalib/AntiKt*SfPtB*.txt") \
                      .restrict_good()


ttbar_r02_trackjets_combined_withchi2 = (ttbar_r02_trackjets).bbb_fit("ttbar_PDF_7b", saveCHI2Fits=True)
ttbar_r02_trackjets_combined = ttbar_r02_trackjets_combined_withchi2.filter(analyses=["ttbar_PDF_7b"])

b_trackjets_extrap = (ttbar_r02_trackjets_combined + ttbar_pre_r02_trackjets + ttbar_r02_trackjets + \
                      ttbar_pre_r04_trackjets + ttbar_r04_trackjets + mcCalib_b_trackjets) \
                     .extrapolate("MCcalib")

####################################
# Track-jets pre-recommendations - c jets
#

## to be added
#wc_sf_r02_trackjets = files("cjets/Wc/AntiKt2PV0TrackJets_W*.txt") \
#                      .restrict()
#wc_sf_r04_trackjets = files("cjets/Wc/AntiKt4PV0TrackJets_W*.txt") \
#                      .restrict()
#charm_trackjets_wc = wc_sf_r02_trackjets + wc_sf_r04_trackjets
#tau_trackjets_wc = charm_trackjets.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")
#mcCalib_ct_trackjets_wc = (files("MCcalib/AntiKt*SfPtC*.txt") + files("MCcalib/AntiKt*SfPtT*.txt")) \
#                          .restrict_good() \
#ct_trackjets_extrap = (charm_trackjets_wc + tau_trackjets_wc + mcCalib_ct_trackjets_wc) \
#                      .extrapolate("Run2MCcalib")


dstar_rebin_template_r02_trackjets = files("commonbinning.txt") \
                                 .filter(analyses=["rebin_dstar_r02_trackjet"])

dstar_rebin_template_trackjets = files("commonbinning.txt") \
                                 .filter(analyses=["rebin_dstar_trackjet"])

ttbar_topo_rebin_r02_trackjets = (dstar_rebin_template_r02_trackjets + ttbar_pre_r02_trackjets + ttbar_r02_trackjets) \
                                 .rebin("rebin_dstar_r02_trackjet", "<>_rebin")

ttbar_topo_rebin_r04_trackjets = (dstar_rebin_template_trackjets + ttbar_pre_r04_trackjets + ttbar_r04_trackjets) \
                                 .rebin("rebin_dstar_trackjet", "<>_rebin")

dstar_trackjets = files("cjets/Dstar/EM/JVF05/AntiKt*.txt") \
                       .restrict_good()

charm_trackjets = (dstar_trackjets + ttbar_topo_rebin_r02_trackjets + ttbar_topo_rebin_r04_trackjets) \
                  .dstar("DStar_<>", "DStar")
                 
tau_trackjets = charm_trackjets.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

mcCalib_ct_trackjets = (files("MCcalib/AntiKt*SfPtC*.txt") + files("MCcalib/AntiKt*SfPtT*.txt")) \
                       .restrict_good() \

ct_trackjets_extrap = (charm_trackjets + tau_trackjets + mcCalib_ct_trackjets) \
                       .extrapolate("MCcalib")

####################################
# Track-jets pre-recommendations - light jets
#

negative_trackjets_pre = files("ljets/negative_tags/pre/AntiKt*.txt") \
                         .restrict_good() \
                         .filter(analyses = ["negative_tags_prerecomm"])

mcCalib_l_trackjets_pre = files("MCcalib/EtaBins/AntiKt*.txt") \
                          .restrict_good() \

light_sf_trackjets_pre = (negative_trackjets_pre + mcCalib_l_trackjets_pre).extrapolate("MCcalib")

####################################
# Track-jets recommendations - light jets
#

light_sf_trackjets = files("ljets/negative_tags/AntiKt2PV0TrackJets_negtag*.txt") \
                     .restrict_good() \
                     .filter(analyses = ["negative_tags"])

####################################
# Track-jets - all together
#

sf_trackjets = b_trackjets_extrap + ct_trackjets_extrap + light_sf_trackjets_pre + light_sf_trackjets


####################################
# The CDI file.
#

master_cdi_file = all_calojets_extrapolated+sf_trackjets
defaultSFs = master_cdi_file.make_cdi("MC15-CDI", "defaults.txt","StandardTag-13TeV-CalibrationFile-25-01-2017-170128215823.root","BtagWP-20161021.root","Continuous_2016-11-17.root","20.7")
master_cdi_file.plot("MC15-CDI", effOnly=True)
master_cdi_file.dump(linage=True, name="master-cdi-linage")
master_cdi_file.plot("MC15-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
(ttbar_pdf_7_combined_withchi2+ttbar_tp_combined_withchi2).plot("MC15-CHi2-Errors")
(sources_ttbar+sources_wc).dump(sysErrors = True, name="sources")
(mcCalib_b_all+mcCalib_ct_all).plot("MC15-MCExtrapolations")

master_cdi_file.make_smooth("MC15-CDI","1","0.4","100")
master_cdi_file.make_nuisance_parameters("MC15-CDI")

# Done!
