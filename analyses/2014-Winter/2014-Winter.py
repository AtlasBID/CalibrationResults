#
# This file runs the fitting for the b-tag combination. Uses a slightly functional syntax to track files
# throught the system.
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

#
# Config for doing the full combination with muon, ttbar, neg tag, and charm
# for the 2014 Lepton Photon Results.
#

title = "Winter 2014 B-Tagging SF Results"
name = "2014-Winter"
description = "Winter 2014 results, based on the full 2012 data"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

taggers = [
#MV1 30% JVF (EM, LC), noJVF (EM, LC)
#    ["MV1", "0.992670537"],
#    ["MV1", "0.994450"],
#MV1 50% JVF (EM, LC), noJVF (EM, LC)
#    ["MV1", "0.992515446"], 
#    ["MV1", "0.993981"], 
#MV1 60% JVF (EM, LC), noJVF (EM, LC)
    ["MV1", "0.9867"], 
    ["MV1", "0.9827 "], 
#MV1 70%
    ["MV1", "0.8119"], 
    ["MV1", "0.7892"], 
#MV1 80%
    ["MV1", "0.3900"], 
    ["MV1", "0.3511"], 
#MV1c 50% JVF (EM, LC)
    ["MV1c", "0.9237"], 
    ["MV1c", "0.9195"], 
#MV1c 57% JVF (EM, LC)
    ["MV1c", "0.8674"], 
    ["MV1c", "0.8641"], 
	
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"],
    ignore=[".*25-pt-30.*",".*300-pt-400.*", ".*system8.*20-pt-30.*"]
    )
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#

s8 = files("system8/*.txt") \
     .restrict()

ptrel = files("ptrel/*.txt") \
	.restrict()
	 
ttdilep_topo = files("topo_ttemu/*.txt") \
               .restrict()

ttbar_pdf_7_all = files("ttbar_pdf/7bins/*.txt") \
                  .restrict() \
                  .filter(analyses = ["PDF_dl_7bins_emu_3jets", "PDF_dl_7bins_emu_2jets", "PDF_dl_7bins_ll_3jets", "PDF_dl_7bins_ll_2jets"])

ttbar_pdf_7_2j = files("ttbar_pdf/7bins/*.txt") \
                  .restrict() \
                  .filter(analyses = ["PDF_dl_7bins_emu_2jets", "PDF_dl_7bins_ll_2jets"])

ttbar_pdf_7_3j = files("ttbar_pdf/7bins/*.txt") \
                  .restrict() \
                  .filter(analyses = ["PDF_dl_7bins_emu_3jets", "PDF_dl_7bins_ll_3jets"])

ttbar_pdf_10_all = files("ttbar_pdf/11bins/*.txt") \
                   .restrict() \
                   .filter(analyses = ["PDF_dilepton_emu_2jets", "PDF_dilepton_emu_3jets", "PDF_dilepton_ll_2jets", "PDF_dilepton_ll_3jets",])

ttbar_pdf_pteta_all = files("ttbar_pdf/pTxEta/*.txt") \
                      .restrict() \
                      .filter(analyses = ["PDF_dl_14bins_emu_2jets", "PDF_dl_14bins_emu_3jets", "PDF_dl_14bins_ll_2jets", "PDF_dl_14bins_ll_3jets",])
                   
                   
ttbar_kinsel_3jet = files("ttbar_kinsel/*/*_em3j.txt") \
                    .restrict()

# We want the 2 jet results as well, but only where they don't overlap with
# Richard's inputs (ttdilep_topo).
ttbar_kinsel_2jet = files("ttbar_kinsel/*/*_em2j.txt") \
                    .restrict() \
                    .filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"])
				  
sources = s8 + ptrel + ttdilep_topo + ttbar_pdf_7_all + ttbar_kinsel_3jet + ttbar_kinsel_2jet + ttbar_pdf_pteta_all + ttbar_pdf_10_all

#
# Build up the central dijet fits. "dijet" is our best estimate, in the end, of the dijet
# fits.
#

dijet = s8

#
# The PDF method comes in bits. We need to put it together in order to
# use it.
#

ttbar_pdf_7_combined = ttbar_pdf_7_all.bbb_fit("PDF_ll_7_fit")
ttbar_pdf_7_combined_2j = ttbar_pdf_7_2j.bbb_fit("PDF_ll_7_2j_fit")
ttbar_pdf_7_combined_3j = ttbar_pdf_7_3j.bbb_fit("PDF_ll_7_3j_fit")
ttbar_pdf_10_combined_extra = ttbar_pdf_10_all.bbb_fit("PDF_ll_10_fit", saveCHI2Fits=True)
ttbar_pdf_10_combined = ttbar_pdf_10_combined_extra.filter(analyses=["PDF_ll_10_fit"])

#
# Do the ttbar results
#  dijet + ttbar topo
#  dijet + ttbar pdf method
#
# ttbar represents all the ttbar fits we are interested in using, in the end.
#

combined_ttbar_topo_extra = (dijet+ttdilep_topo+ttbar_kinsel_3jet+ttbar_kinsel_2jet).bbb_fit("ttbar_topo_dijet", saveCHI2Fits=True, includeSources = True)
combined_ttbar_pdf_extra = (dijet+ttbar_pdf_10_all).bbb_fit("ttbar_pdf_dijet", saveCHI2Fits=True, includeSources = True)
ttbar_pdf_pteta_extra = ttbar_pdf_pteta_all.bbb_fit("PDF_14bins", saveCHI2Fits=True, includeSources = True)

combined_ttbar_topo = combined_ttbar_topo_extra.filter(analyses = ["ttbar_topo_dijet"])
combined_ttbar_pdf = combined_ttbar_pdf_extra.filter(analyses = ["ttbar_pdf_dijet"])
ttbar_pdf_pteta = ttbar_pdf_pteta_extra.filter(analyses = ["PDF_14bins"])

ttbar = combined_ttbar_topo + combined_ttbar_pdf + ttbar_pdf_7_combined + ttbar_pdf_10_combined + ttbar_pdf_7_combined_2j + ttbar_pdf_7_combined_3j

ttbar_pdf_dijet_simple_combo = (ttbar_pdf_10_combined+dijet).bbb_fit("ttbar_pdf_dijet_simple", saveCHI2Fits=True, includeSources=True)

#combined_ttbar_topo_chi2 = combined_ttbar_topo_extra.filter(analyses = ["comb_ttbar_topo_dijet_temp"])
#combined_ttbar_pdf_chi2 = combined_ttbar_pdf_extra.filter(analyses = ["comb_ttbar_pdf_dijet_temp"])
#ttbar_pdf_pteta_chi2 = ttbar_pdf_pteta_extra.filter(analyses = ["comb_PDF_14bins_temp"])

#
# Next, we need to build up the master fits that will be used to make charm and tau results.
# This requires re-binning to match the D* input bins.
#
#
# The file "commonbinning.txt" just contains some empty specifications that have the binning. They don't contain
# any real data. It should have the same binning as the D*. The _30 is without the 20-30 to deal with the PDF method,
# which has a bin we ignore from 25-30, and that bin can't really participate.
#

rebin_template = files("commonbinning.txt") \
                 .filter(analyses=["rebin"])
rebin_template_30 = files("commonbinning.txt") \
                    .filter(analyses=["rebin_30"])

ttbar_rebin = (rebin_template + ttbar) \
              .rebin("rebin", "<>_rebin")
              
#Can't do a S8 only guy because the low bin is missing!
#dijet_rebin = (rebin_template + dijet) \
#              .rebin("rebin", "<>_rebin")

####################################
# Tau and Charm
#

# Calculate the new D* values for charm. Use the algorithm provided by Fabrizio.
# The tau is just an additional error on top of that.
#

dstar_template = files("DStar/*/*.txt") \
                 .restrict()

charm_sf_ttbar = (dstar_template + ttbar_rebin) \
                 .dstar("DStar_<>", "DStar")

#charm_sf_dijet = (dstar_template + dijet_rebin) \
#                 .dstar("DStar_<>", "DStar")
                 
charm_sf = charm_sf_ttbar
#+ charm_sf_dijet

                 
tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources += dstar_template

####################################
# Light SF come from the negative tags
#

negative = files("negative/*.txt") \
           .restrict()

light_sf = negative

sources += negative

####################################
# Plotting

#
# Plot the dijet and the main ttbar fit for comparison as well
#

combined_ttbar_topo_extra.plot("ttbar_topo_chi2")
combined_ttbar_pdf_extra.plot("ttbar_pdf_chi2")
ttbar_pdf_pteta_extra.plot("ttbar_pdf_peta_chi2")
(ttbar_pdf_10_all+ttbar_pdf_10_combined_extra).plot("ttbar_pdf_only_chi2", effOnly=True)
ttbar_pdf_dijet_simple_combo.plot("ttbar_pdf_dijet_simple_chi", effOnly=True)

(ttbar_pdf_7_combined+ttbar_pdf_10_combined).plot("ttbar_pdf_7_10")
ttbar_pdf_7_combined.plot("ttbar_pdf_7")
ttbar_pdf_10_combined.plot("ttbar_pdf_10")

(ptrel + s8).plot("dijet")

#
# Plot the fit ttbar results
#

#(ttbar_pdf_7_combined + ttbar_pdf_7_precomb).plot("ttdlep_pdf_compare")

#
# Extrapolate everything
#

mcCalib = files("MCcalib/*.txt") \
    .restrict() \
    .filter(ignore=[".*20-pt-30.*"])

all_extrapolated = (\
        dijet \
        + mcCalib \
        ) \
        .extrapolate("MCcalib")

####################################
# The CDI file.
#

master_cdi_file = \
    ttbar_pdf_pteta \
        + ttbar\
        + charm_sf \
        + tau_sf \
        + light_sf \
    + all_extrapolated \
    + sources
defaultSFs = master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "MCefficiencies_for_CDI_14.4.2013.root")
master_cdi_file.plot("MC12-CDI")
master_cdi_file.plot("MC12-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
sources.dump(sysErrors = True, name="sources")

(master_cdi_file + defaultSFs).plot("MC12-ByTagger", byCalibEff = True, effOnly=True)

# Done!
