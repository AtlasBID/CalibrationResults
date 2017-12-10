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
#60%
    ["MV2c10",    "FixedCutBEff_60"],
    ["MV2c10mu",  "FixedCutBEff_60"],
    ["MV2c10rnn", "FixedCutBEff_60"],
    ["DL1",       "FixedCutBEff_60"],
    ["DL1mu",     "FixedCutBEff_60"],
    ["DL1rnn",    "FixedCutBEff_60"],
    ["MV2c10",    "HybBEff_60"],
    ["MV2c10mu",  "HybBEff_60"],
    ["MV2c10rnn", "HybBEff_60"],
    ["DL1",       "HybBEff_60"],
    ["DL1mu",     "HybBEff_60"],
    ["DL1rnn",    "HybBEff_60"],
#70%
    ["MV2c10",    "FixedCutBEff_70"],
    ["MV2c10mu",  "FixedCutBEff_70"],
    ["MV2c10rnn", "FixedCutBEff_70"],
    ["DL1",       "FixedCutBEff_70"],
    ["DL1mu",     "FixedCutBEff_70"],
    ["DL1rnn",    "FixedCutBEff_70"],
    ["MV2c10",    "HybBEff_70"],
    ["MV2c10mu",  "HybBEff_70"],
    ["MV2c10rnn", "HybBEff_70"],
    ["DL1",       "HybBEff_70"],
    ["DL1mu",     "HybBEff_70"],
    ["DL1rnn",    "HybBEff_70"],
#77%
    ["MV2c10",    "FixedCutBEff_77"],
    ["MV2c10mu",  "FixedCutBEff_77"],
    ["MV2c10rnn", "FixedCutBEff_77"],
    ["DL1",       "FixedCutBEff_77"],
    ["DL1mu",     "FixedCutBEff_77"],
    ["DL1rnn",    "FixedCutBEff_77"],
    ["MV2c10",    "HybBEff_77"],
    ["MV2c10mu",  "HybBEff_77"],
    ["MV2c10rnn", "HybBEff_77"],
    ["DL1",       "HybBEff_77"],
    ["DL1mu",     "HybBEff_77"],
    ["DL1rnn",    "HybBEff_77"],
#85%
    ["MV2c10",    "FixedCutBEff_85"],
    ["MV2c10mu",  "FixedCutBEff_85"],
    ["MV2c10rnn", "FixedCutBEff_85"],
    ["DL1",       "FixedCutBEff_85"],
    ["DL1mu",     "FixedCutBEff_85"],
    ["DL1rnn",    "FixedCutBEff_85"],
    ["MV2c10",    "HybBEff_85"],
    ["MV2c10mu",  "HybBEff_85"],
    ["MV2c10rnn", "HybBEff_85"],
    ["DL1",       "HybBEff_85"],
    ["DL1mu",     "HybBEff_85"],
    ["DL1rnn",    "HybBEff_85"],
#DL1 c-tagger
    ["DL1rnn", "CTag_Tight"],
    ["DL1rnn", "CTag_Loose"],
#MV2 c-tagger
    ["MV2cl100_MV2c100", "CTag_Tight"],
    ["MV2cl100_MV2c100", "CTag_Loose"],
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

# recommendations from release 21
ttbar_pdf_7_sf = files("bjets/ttbar_pdf/btag*.txt") \
                 .restrict() \
                 .filter(analyses = ["ttbar_PDF"])

# extrapolation
mcCalib_b = files("extrap/MCcalibCDI_Zprimebb5000_b*.txt") \
            .restrict()

ttbar_pdf_extrap = (mcCalib_b + ttbar_pdf_7_sf) \
                    .extrapolate("Run2MCcalib")

sources_bjets = ttbar_pdf_7_sf


####################################
# c-jets

# pre-recommendations from release 20.7
pre_ttc_sf = files("cjets/ttbarC/pre/*txt") \
            .restrict()

# recommendations from release 21
ttc_sf = files("cjets/ttbarC/ctag_*") \
         .restrict() \
         .filter(analyses = ['ttbarC'])


# extrapolation to high pT
mcCalib_c = files("extrap/ttC_MCcalibCDI_ttbar_c*") + files("extrap/ttC_MCcalibCDI_ttbar_t*") \
            .restrict()

ttc_sf_extrap = (mcCalib_c + ttc_sf) \
                    .extrapolate("Run2MCcalib_ttC")

sources_cjets = ttc_sf

####################################
# tau-jets

# extrapolation to tau-jets
pre_ttc_tau_sf = pre_ttc_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

# extrapolation to high pT
pre_ttc_tau_sf_extrap = (mcCalib_c + pre_ttc_tau_sf) \
                        .extrapolate("Run2MCcalib_ttC")

####################################
# light-jets


# recommendations from release 21

negative_tag_Zjet_sf = files("ljets/negative_tags/NegTagZjets*.txt") \
                       .restrict() \
                       .filter(analyses = ["negative_tag_Zjet"])  

negative_tags_sf = files("ljets/negative_tags/negtag*.txt") \
                       .restrict() \
                       .filter(analyses = ["negative_tags"])  


# pre-recommendations from release 20.7
#pre_negative_sf = files("ljets/negative_tags/pre/*txt") \
#              .restrict_good()

sources_ljets = negative_tag_Zjet_sf + negative_tags_sf 

###### c-tagger ##########

cTag_ttbar_pdf_7_all = (files("ctagger/bjets/ttbar_pdf/*emu*7bins*.txt") \
                   + files("ctagger/bjets/ttbar_pdf/*ll*7bins*.txt")) \
                  .restrict() \
                  .filter(analyses = ["PDF_6bins_emu_2j", "PDF_6bins_emu_3j", \
                                      "PDF_6bins_ll_2j",  "PDF_6bins_ll_3j"])

cTag_ttbar_pdf_7_2j = cTag_ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_emu_2j", "PDF_6bins_ll_2j"])

cTag_ttbar_pdf_7_3j = cTag_ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_emu_3j", "PDF_6bins_ll_3j"])

cTag_ttbar_pdf_7_combined_withchi2 = (cTag_ttbar_pdf_7_all).bbb_fit("cTag_ttbar_pdf_7b", saveCHI2Fits=True)
cTag_ttbar_pdf_7_combined = cTag_ttbar_pdf_7_combined_withchi2.filter(analyses=["cTag_ttbar_pdf_7b"])

cTag_ttbar_pdf_fits = cTag_ttbar_pdf_7_combined

cTag_mcCalib_b_all = files("ctagger/extrapolate/MCcalibCDI*Zprimebb5000_b*.txt") \
                .restrict()

cTag_ttbar_extrapolated = (cTag_mcCalib_b_all \
                      + cTag_ttbar_pdf_fits ) \
                      .extrapolate("Run2MCcalib")

### light jets
cTag_mcbased_sf = files("ctagger/lightjets/MCBased*.txt") \
             .restrict()

# charm jets

cTag_ttc_sf = files("ctagger/cjets/ttbarC/*.txt") \
              .restrict()

cTag_tau_ttc_sf = cTag_ttc_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")


cTag_mcCalib_ttc = files("ctagger/extrapolate/ttC_MCcalibCDI*ttbar_c*") + files("ctagger/extrapolate/ttC_MCcalibCDI*ttbar_t*") \
              .restrict()

cTag_ttc_sf_extrapolated = (cTag_mcCalib_ttc + cTag_ttc_sf) \
                       .extrapolate("Run2MCcalib_ttC")

cTag_tau_ttc_sf_extrapolated = (cTag_mcCalib_ttc + cTag_tau_ttc_sf) \
                           .extrapolate("Run2MCcalib_ttC")

all_cTag_calojets =  cTag_ttbar_extrapolated + cTag_mcbased_sf + cTag_ttc_sf_extrapolated + cTag_tau_ttc_sf_extrapolated

####################################
# all together for calo-jets

all_calojets = ttbar_pdf_extrap \
               + ttc_sf_extrap \
               + pre_ttc_tau_sf_extrap \
               + negative_tag_Zjet_sf + negative_tags_sf + all_cTag_calojets


####################################
# The CDI file.

master_cdi_file = all_calojets
defaultSFs = master_cdi_file.make_cdi("MC16-CDI", "defaults.txt","2017-13TeV-EfficiencyMapsOnly-Release21-AntiKt4EMTopoJets-Aug3.root","2017-13TeV-WorkingPointsOnly-Release21-AntiKt4EMTopoJets-July27.root","21")
master_cdi_file.plot("MC16-CDI", effOnly=True)
master_cdi_file.dump(linage=True, name="master-cdi-linage")
master_cdi_file.plot("MC16-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
(sources_bjets+sources_cjets+sources_ljets).dump(sysErrors = True, name="sources")

master_cdi_file.make_smooth("MC16-CDI","1","0.4","100")
master_cdi_file.make_nuisance_parameters("MC16-CDI")

# Done!
