#
# Want to get rid of this eventually...
#

from files import files

#
# Config for doing the full combination with muon, ttbar, neg tag, and charm
# for the 2012 Paper.
#

title = "Spring 2013 B-Tagging SF Results - LHCP"
name = "2013-LHCP"
description = "Spring 2013 results, based on the full 2012 data, for LHCP"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

taggers = [
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
# Input arguments
#

s8 = files("system8/*.txt") \
     .filter(taggers=taggers) \
     .filter(ignore=[".*JVF0_5.*"])

ttdilep_emu_pdf = files("pdfmethod_ttdilep/*.txt") \
                  .filter(analyses = ["PDF_dilepton_emu_3jets", "PDF_dilepton_emu_2jets"]) \
                  .filter(taggers=taggers)
ttdilep_ll_pdf = files("pdfmethod_ttdilep/*.txt") \
                 .filter(analyses = ["PDF_dilepton_ll_3jets", "PDF_dilepton_ll_2jets"]) \
                 .filter(taggers=taggers)
ttdilep_g_rebined_pdf = files("pdfmethod_ttdilep_rebin/*.txt") \
                        .filter(taggers=taggers)

ttdilep_topo = files("topo_ttemu/*.txt") \
               .filter(taggers=taggers) \
               .filter(ignore=[".*25-pt-30.*"])

#
# Some checks
#

ttdilep_topo.dump(check=True)

#
# Fit the guys
#

#fit_ttdilep_emu_pdf = ttdilep_emu_pdf.fit("ttbar_dilep_emu_fit")
fit_ttdilep_ll_pdf = ttdilep_ll_pdf.bbb_fit("PDF_dilepton_ll_fit")
fit_ttdilep_emu_pdf = ttdilep_emu_pdf.bbb_fit("PDF_dilepton_emu_fit")

#
# Put the fit_ttdilep and S8 on equal footing - for plotting purposes only.
#
rebin_template = files("commonbinning.txt") \
                 .filter(analyses=["rebin"])
rebin_template_30 = files("commonbinning.txt") \
                    .filter(analyses=["rebin_30"])

fit_ttdilep_ll_s8_binning = (fit_ttdilep_ll_pdf + rebin_template) \
                         .rebin("rebin", "PDF_dilepton_ll_fit_rebin")
fit_ttdilep_emu_s8_binning = (fit_ttdilep_emu_pdf + rebin_template) \
                         .rebin("rebin", "PDF_dilepton_emu_fit_rebin")
s8_rebinned = (rebin_template + s8) \
              .rebin("rebin", "system8_rebin")

tt_topo = (rebin_template_30 + ttdilep_topo) \
          .rebin("rebin_30", "ttbar_topo_emu_rebin")

#
# Calculate the new D* values for charm.
#

dstar_template = files("DStar/*.txt")
char_sf = (dstar_template + fit_ttdilep_ll_s8_binning + fit_ttdilep_emu_s8_binning).dstar("DStar_<>", "DStar")
char_sf.plot("charm")

#
# Plot the two fits so we can compare them (well).
#

(fit_ttdilep_ll_pdf + fit_ttdilep_emu_pdf).plot("pdf_method_fits")
(ttdilep_ll_pdf + ttdilep_emu_pdf + fit_ttdilep_ll_pdf + fit_ttdilep_emu_pdf).plot("pdf_method_all")

(ttdilep_g_rebined_pdf + fit_ttdilep_emu_s8_binning).plot("rebin_test")

#
# Plot the dijet and the main ttbar fit for comparison as well
#

(fit_ttdilep_emu_s8_binning + tt_topo + s8_rebinned).plot("tts8_compare")


TrigTagBuilder = [
#    ["", "-999"],
#    ["JetFitterCOMBNN", "2.20"],
#    ["JetFitterCOMBNN", "-1.25"],
    ]

TrigTagDataInfo = [
#    "TrigTight%s_BE",
#    "TrigTight%s_KL1",
#    "TrigTight%s_L2M",
#    "TrigMedium%s_BE",
#    "TrigMedium%s_KL1",
#    "TrigMedium%s_L2M",
    ]

for tt in TrigTagDataInfo:
    for tbld in TrigTagBuilder:
        tname = tbld[0]
        if len(tname) != 0:
            tname = "_%s" % tname
        s = [tt % tname, tbld[1]]
        taggers.append(s)

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
# Analysis Groupings - how we want the combination to run
#

analysisGroupings = {
    'bottom': {
		'ttbar_dilep_emu_fit': ["PDFmethod_dilepton_emu_2jets", "PDFmethod_dilepton_emu_3jets"],
		'ttbar_ll': ["PDFmethod_dilepton_ll_2jets", "PDFmethod_dilepton_ll_3jets"],
	},
}

# DO both a bin-by-bin fit and a profile fit.
CombinationTypeInfo = [
    { "type": "binbybin", "prefix" : "bbb_" },
    { "type": "profile", "prefix" : "" }
]

# Use the bin-by-bin fit, and the difference in the error
DifferenceAsError = [
    { "ResultCalib" : "ttbar_dilep_emu",
      "BaselineCalib" : "bbb_ttbar_dilep_emu_fit",
      "DeltaCalib" : "ttbar_dilep_emu_fit",
      "SystematicError" : "Correlated Uncorrelated Fit Delta"
      }
    ]

#
# List of guys that we are going to ignore during our
# running
#
ignore_analyses = [
# These are extra bins put in by ptrel, which we don't
# want to use in a fit.
    ".*:20-pt-200:.*", 

# Some ttbar analyses start funny, but all bins must match, so
# we have to ignore the half bins.
    ".*:25-pt-30:.*",

# There are a number of OPs that are in the calibration files that shouldn't be in the
# calibration files.
    ]

#
# The root file that we start everything with.
#

mcEffRootFile = "MCefficiencies_for_CDI_14.4.2013.root"
CDIFile = "%s-MC12-CDI.root" % name

#
# Should we avoid the combination?
#

runCombination = True
