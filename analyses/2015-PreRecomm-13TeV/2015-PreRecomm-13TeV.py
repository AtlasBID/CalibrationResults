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

taggers = [
#MV1 50% JVF (EM)
    ["MV1", "0.992515446"],
#MV1 60% JVF (EM)
    ["MV1", "0.9867"],
#MV1 70% JVF (EM)
    ["MV1", "0.8119"],
#MV1 80% JVF (EM)
    ["MV1", "0.3900"],
#MV1 85% JVF (EM)
    ["MV1", "0.1644"],
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict_good = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4TopoEMJVF0_5"],
    ).verify_OPs("8TeV")

sfObject.restrict_ignore = lambda self: self.filter(
    ignore=[".*25-pt-30.*",".*300-pt-400.*"]
    )
	
sfObject.restrict = lambda self: self.restrict_good().restrict_ignore()
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#


ttbar_pdf_7_all = (files("ttbar_pdf/EM/*/*/*6bins.txt")) \
                  .restrict() \
                  .filter(analyses = ["PDF_6bins_emu_2jets", "PDF_6bins_emu_3jets", \
                                      "PDF_6bins_ll_2jets", "PDF_6bins_ll_3jets", \
                                      ])

ttbar_pdf_7_2j = ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_ll_2jets", "PDF_6bins_emu_2jets", \
                                     ])

ttbar_pdf_7_3j = ttbar_pdf_7_all \
                 .filter(analyses = ["PDF_6bins_ll_3jets", "PDF_6bins_emu_3jets", \
                                     ])
				  					
ttbar_pdf_10_all = (files("ttbar_pdf/EM/*/10PT*/*jets.txt")) \
                   .restrict() \
                   .filter(analyses = ["PDF_emu_2jets", "PDF_emu_3jets", \
                                       "PDF_ll_2jets", "PDF_ll_3jets", \
                                       ]) \

ttbar_pdf_10_2j = ttbar_pdf_10_all \
                  .filter(analyses = ["PDF_ll_2jets", "PDF_emu_2jets", \
                                      ])

ttbar_pdf_10_3j = ttbar_pdf_10_all \
                  .filter(analyses = ["PDF_emu_3jets", "PDF_ll_3jets", \
                                      ])

sources_7  = ttbar_pdf_7_all
sources_10 = ttbar_pdf_10_all


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

ttbar_pdf_10_combined = ttbar_pdf_10_all.bbb_fit("ttbar_PDF_10b")
ttbar_pdf_10_combined_2j = ttbar_pdf_10_2j.bbb_fit("ttbarPDF10b2j")
ttbar_pdf_10_combined_3j = ttbar_pdf_10_3j.bbb_fit("ttbarPDF10b3j")

# one ring to rule them all...
ttbar_fits_7 = ttbar_pdf_7_combined \
    + ttbar_pdf_7_combined_2j \
    + ttbar_pdf_7_combined_3j

ttbar_fits_10 = \
	+ ttbar_pdf_10_combined \
	+ ttbar_pdf_10_combined_2j \
	+ ttbar_pdf_10_combined_3j

ttbar_fits = ttbar_fits_7 + ttbar_fits_10

#
# Next, we need to build up the master fits that will be used to make charm and tau results.
# This requires re-binning to match the D* input bins (for both charm and tau, as they
# are just versions of each other).
# Use one of the D* results as the rebin template.
#

dstar_rebin_template = files("Dstar/EM/JVF05/DStar_MV170.txt")

ttbar_rebin = (dstar_rebin_template + ttbar_fits) \
              .rebin("DStar", "<>_rebin")


####################################
# Tau and Charm
#

# Calculate the new D* values for charm. Use the algorithm provided by Fabrizio.
# The tau is just an additional error on top of that.
#

dstar_template = (files("Dstar/*/JVF05/*.txt") + files("Dstar/*/noJVF/*.txt")) \
                 .restrict()

charm_sf = (dstar_template + ttbar_rebin) \
           .dstar("DStar_<>", "DStar")
                 
tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources_4 = dstar_template

####################################
# Light SF come from the negative tags
#

negative = (files("negative_tags/*/JVF05/*.txt")) \
           .restrict()

light_sf = negative

# We'd like to do this, but we can't extrapolate accross bin boundaries.
#sources_10 += negative


####################################
# Extrapolate everything
#

mcCalib_bct = (files("MCcalib/SfPtB*.txt") + files("MCcalib/SfPtC*.txt") + files("MCcalib/SfPtT*.txt")) \
              .restrict_good() \
              .filter(ignore=[".*15-pt-20.*",".*20-pt-30.*",".*30-pt-40.*",".*40-pt-50.*",".*50-pt-60.*"])
	
mcCalib_l =  files("MCcalib/EtaBins/SfPtL*.txt") \
            .restrict_good() \
            .filter(ignore=[".*15-pt-20.*",".*20-pt-30.*",".*30-pt-40.*",".*40-pt-50.*",".*50-pt-60.*",".*60-pt-75.*",".*75-pt-90.*",".*90-pt-110.*",".*110-pt-140.*",".*140-pt-200.*",".*200-pt-300.*"])
 
rebin_template_high = rebin_template_all \
    .filter(ignore=[".*20-pt-30.*"])

mcCalib_rebin_bct = (rebin_template_high + mcCalib_bct) \
    .rebin("rebin", "<>_rebin")

rebin_for_extrap_dstar = files("commonbinning.txt") \
                       .filter(analyses=["rebin_dstar"])

mcCalib_rebin_dstar_bct = (rebin_for_extrap_dstar + mcCalib_bct) \
    .rebin("rebin_dstar", "<>_rebin")

default_extrapolated = (\
    ttbar_fits_10 \
    + mcCalib_bct \
    + sources_10
    ) \
    .extrapolate("MCcalib")

#	+ light_sf \
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

all_extrapolated = default_extrapolated + rebin_extrapolated + rebin_dstar_extrapolated + light_extrapolated

# Currently can't extrapolate:
#  neg tags - because they are split in eta, and the extrapolation isn't.

####################################
# The CDI file.
#

master_cdi_file = \
    all_extrapolated \
	+ trigger
defaultSFs = master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "StandardTag_8TeV_ttbar_140613151009.root")
master_cdi_file.plot("MC12-CDI", effOnly=True)
master_cdi_file.dump(linage=True, name="master-cdi-linage")
master_cdi_file.plot("MC12-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
(ttbar_pdf_7_combined_withchi2).plot("MC12-CHi2-Errors")
(sources_7+sources_10+sources_4).dump(sysErrors = True, name="sources")

#(master_cdi_file + defaultSFs).plot("MC12-ByTagger", byCalibEff = True, effOnly=True)

# Done!