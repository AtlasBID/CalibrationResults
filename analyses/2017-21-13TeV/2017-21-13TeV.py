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

title = "Recommendations of flavor tagging results for release 21"
name = "2017-21-13TeV"
description = "Flavor tagging recommendations for release 21"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

taggers = [
#MV2c10 60%
    ["MV2c10", "FixedCutBEff_60"],
#MV2c10 70%
    ["MV2c10", "FixedCutBEff_70"],
#MV2c10 77%
    ["MV2c10", "FixedCutBEff_77"],
#MV2c10 85%
    ["MV2c10", "FixedCutBEff_85"],
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict_good = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4EMTopoJets"],
    ).verify_OPs("21")

sfObject.restrict_ignore = lambda self: self.filter(
    ignore=[".*25-pt-30.*"]
    )

sfObject.restrict_ignore_tight = lambda self: self.filter(
    ignore=[".*25-pt-30.*",".*200-pt-300.*",".*250-pt-300.*",".*300-pt-400.*"]
    )


sfObject.restrict = lambda self: self.restrict_good().restrict_ignore()

sfObject.restrict_tight = lambda self: self.restrict_good().restrict_ignore_tight()

	
####################################
# b-jets 

# pre-recommendations from release 20.7
pre_ttbar_pdf_7_sf = files("bjets/ttbar_pdf/pre/*.txt") \
                     .restrict() \
                     .filter(analyses = ["PDF_6bins_emu_2j", "PDF_6bins_emu_3j", \
                                         "PDF_6bins_ll_2j",  "PDF_6bins_ll_3j"])

# combination 
pre_ttbar_pdf_7_combined_withchi2 = (pre_ttbar_pdf_7_sf).bbb_fit("pre_ttbar_PDF_7b", saveCHI2Fits=True)
pre_ttbar_pdf_7_combined = pre_ttbar_pdf_7_combined_withchi2.filter(analyses=["pre_ttbar_PDF_7b"])

# extrapolation
mcCalib_b = files("extrap/MCcalibCDI_Zprimebb5000_b*.txt") \
            .restrict()

pre_ttbar_pdf_extrap = (mcCalib_b + pre_ttbar_pdf_7_combined) \
                       .extrapolate("Run2MCcalib")

sources_bjets = pre_ttbar_pdf_7_sf


####################################
# c-jets

# pre-recommendations from release 20.7
pre_ttc_sf = files("cjets/ttbarC/pre/*txt") \
            .restrict()

# extrapolation to high pT
mcCalib_c = files("extrap/ttC_MCcalibCDI_ttbar_c*") + files("extrap/ttC_MCcalibCDI_ttbar_t*") \
            .restrict()

pre_ttc_sf_extrap = (mcCalib_c + pre_ttc_sf) \
                    .extrapolate("Run2MCcalib_ttC")

sources_cjets = pre_ttc_sf

####################################
# tau-jets

# extrapolation to tau-jets
pre_ttc_tau_sf = pre_ttc_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

# extrapolation to high pT
pre_ttc_tau_sf_extrap = (mcCalib_c + pre_ttc_tau_sf) \
                        .extrapolate("Run2MCcalib_ttC")

####################################
# light-jets

# pre-recommendations from release 20.7
pre_negative_sf = files("ljets/negative_tags/pre/*txt") \
              .restrict_good()

sources_ljets = pre_negative_sf

####################################
# all together for calo-jets

all_calojets = pre_ttbar_pdf_extrap \
               + pre_ttc_sf_extrap \
               + pre_ttc_tau_sf_extrap \
               + pre_negative_sf


####################################
# The CDI file.

master_cdi_file = all_calojets
defaultSFs = master_cdi_file.make_cdi("MC16-CDI", "defaults.txt","StandardTag-13TeV-CalibrationFile-05-06-2017.root","BtagWP-20170514.root","21")
master_cdi_file.plot("MC16-CDI", effOnly=True)
master_cdi_file.dump(linage=True, name="master-cdi-linage")
master_cdi_file.plot("MC16-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
(sources_bjets+sources_cjets+sources_ljets).dump(sysErrors = True, name="sources")

master_cdi_file.make_smooth("MC16-CDI","1","0.4","100")
master_cdi_file.make_nuisance_parameters("MC16-CDI")

# Done!
