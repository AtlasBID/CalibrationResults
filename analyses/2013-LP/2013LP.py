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
    ["MV1", "0.992670537"],
    ["MV1", "0.994450"],
#MV1 50% JVF (EM, LC), noJVF (EM, LC)
    ["MV1", "0.992515446"], 
    ["MV1", "0.993981"], 
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
    jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"],
    ignore=[".*25-pt-30.*"]
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
                  .filter(analyses = ["PDFmethod_dilepton_7bins_emu_3jets", "PDFmethod_dilepton_7bins_emu_2jets", "PDFmethod_dilepton_7bins_ll_3jets", "PDF_dilepton_7bins_ll_2jets"])

ttbar_pdf_7_precomb = files("ttbar_pdf/7bins/*.txt") \
                      .restrict() \
                      .filter(analyses = ["PDFmethod_dilepton_emu_2and3jets"])
               
sources = s8 + ttdilep_topo + ttbar_pdf_7_all

#
# Where we can, we should combine Richards ttbar and s8 results. "all" is what will go
# into the CDI below.
#

dijet = s8
ttbar = ttdilep_topo
all = (dijet+ttbar).bbb_fit("ttbar_dijet")

#
# Next, fit together the pdf ttbar results (ffit == full fit)
#

ttbar_pdf_7_combined = ttbar_pdf_7_all.bbb_fit("PDF_dilepton_fit")
all += ttbar_pdf_7_combined

#
# Due to the binning it isn't really possible to compare these fits. So, go for the lowest common
# denominator - s8 binning - and refit the ttbar results to fit that model. Then we can plot them together.
# This isn't going to be the most accurate version, but it will be close enough.
#
# Some of the rebinned results below will also be used for the D* recalculation (which requires the fitting).
#
# The file "commonbinning.txt" just contains some empty specifications that have the binning. They don't contain
# any real data. :-)
#

rebin_template = files("commonbinning.txt") \
                 .filter(analyses=["rebin"])
rebin_template_30 = files("commonbinning.txt") \
                    .filter(analyses=["rebin_30"])

#fit_ttdilep_ll_s8_binning = (fit_ttdilep_ll_pdf + rebin_template) \
#    .rebin("rebin", "PDF_dilepton_ll_fit_rebin")
#fit_ttdilep_emu_s8_binning = (fit_ttdilep_emu_pdf + rebin_template) \
#                         .rebin("rebin", "PDF_dilepton_emu_fit_rebin")
# Rebinning this traditional ttbar results is hard because the low bin is 25-30, not 20-30 as the D* analysis requires
#ttdilep_topo_rebinned = (ttdilep_topo + rebin_template) \
#                        .rebin("rebin", "ttbar_topo_emu_rebin")
s8_rebinned = (rebin_template + s8) \
              .rebin("rebin", "system8_rebin")
all_rebin = (all + rebin_template) \
              .rebin("rebin", "ttbar_dijet_rebin")
tt_topo = (rebin_template_30 + ttdilep_topo) \
          .rebin("rebin_30", "ttbar_topo_emu_rebin")

          
####################################
# Tau and Charm
#

# Calculate the new D* values for charm. Use the algorithm provided by Fabrizio.
# The tau is just an additional error on top of that.
#

dstar_template = files("DStar/*/*.txt") \
                 .restrict()

charm_sf = (dstar_template + s8_rebinned + all_rebin) \
    .dstar("DStar_<>", "DStar")

tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources += dstar_template

####################################
# Light SF come from the negative tags
#

negative = files("negative/*.txt") \
           .restrict()

sources += negative

####################################
# Plotting

#
# Plot the dijet and the main ttbar fit for comparison as well
#

(tt_topo + s8_rebinned).plot("tts8_compare")

#
# Plot the fit ttbar results
#

(ttbar_pdf_7_combined+ttbar_pdf_7_precomb).plot("ttdlep_pdf_compare")

####################################
# The CDI file.
#

master_cdi_file = \
    dijet + ttbar + all \
    + charm_sf \
    + tau_sf \
    + negative
master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "MCefficiencies_for_CDI_14.4.2013.root")
master_cdi_file.plot("MC12-CDI")
master_cdi_file.dump(sysErrors = True, name="master")
sources.dump(sysErrors = True, name="sources")

# Done!