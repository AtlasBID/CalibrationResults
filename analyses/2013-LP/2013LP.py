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
# for the 2012 Lepton Photon Results.
#

title = "Spring 2013 B-Tagging SF Results - Lepton-Photon"
name = "2013-LP"
description = "Spring 2013 results, based on the full 2012 data, for Lepton Photon"

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
#    ["MV1c", "0.9237"], 
#    ["MV1c", "0.9195"], 
#MV1c 57% JVF (EM, LC)
#    ["MV1c", "0.8674"], 
#    ["MV1c", "0.8641"], 
	
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"],
    ignore=[".*25-pt-30.*",".*300-pt-400.*"]
    )
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#

s8 = files("system8/*.txt") \
     .restrict()

ttdilep_topo = files("topo_ttemu/*.txt") \
               .restrict()

ttbar_pdf_7_all = files("ttbar_pdf/7bins/*.txt") \
                  .restrict() \
                  .filter(analyses = ["PDF_dilepton_7bins_emu_3jets", "PDF_dilepton_7bins_emu_2jets", "PDF_dilepton_7bins_ll_3jets", "PDF_dilepton_7bins_ll_2jets"])

ttbar_pdf_7_precomb = files("ttbar_pdf/7bins/*.txt") \
                      .restrict() \
                      .filter(analyses = ["PDF_dilepton_emu_2and3jets"])
               
ttbar_pdf_10_all = files("ttbar_pdf/11bins/*.txt") \
                  .restrict()

sources = s8 + ttdilep_topo + ttbar_pdf_7_all

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
ttbar_pdf_10_combined = ttbar_pdf_10_all.bbb_fit("PDF_ll_10_fit")

#
# Do the ttbar results
#  dijet + ttbar topo
#  dijet + ttbar pdf method
#
# ttbar represents all the ttbar fits we are interested in using, in the end.
#

combined_ttbar_topo = (dijet+ttdilep_topo).bbb_fit("ttbar_topo_dijet")
combined_ttbar_pdf = (dijet+ttbar_pdf_10_all).bbb_fit("ttbar_pdf_dijet")

ttbar = combined_ttbar_topo + combined_ttbar_pdf

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

dijet_for_charm = dijet
                 .filter(jets=["AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"])
charm_sf_dijet = (dstar_template + dijet_for_charm) \
                 .dstar("DStar_<>", "DStar")

charm_sf = charm_sf_ttbar + charm_sf_dijet

                 
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

#(tt_topo + s8_rebinned).plot("tts8_compare")

#
# Plot the fit ttbar results
#

#(ttbar_pdf_7_combined + ttbar_pdf_7_precomb).plot("ttdlep_pdf_compare")

####################################
# The CDI file.
#

master_cdi_file = \
    dijet + ttbar \
    + charm_sf \
    + tau_sf \
    + light_sf
master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "MCefficiencies_for_CDI_14.4.2013.root")
master_cdi_file.plot("MC12-CDI")
master_cdi_file.dump(sysErrors = True, name="master")
sources.dump(sysErrors = True, name="sources")

# Done!
