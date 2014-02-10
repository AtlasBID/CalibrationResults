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
#MV1 60% JVF (EM, LC)
    ["MV1", "0.9867"], 
    ["MV1", "0.9827 "], 
#MV1 70% JVF (EM, LC)
    ["MV1", "0.8119"], 
    ["MV1", "0.7892"], 
#MV1 80% JVF (EM, LC)
    ["MV1", "0.3900"], 
    ["MV1", "0.3511"],
#MV1 85% JVF (LC)
    ["MV1", "0.1340"],     
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
    ignore=[".*25-pt-30.*",".*300-pt-400.*", ".*system8.*20-pt-30.*", ".*MV1-0.1340-AntiKt4TopoLCnoJVF.*"]
    )
	
####################################
# Bottom Flavor Inputs and fits
#  Note: sources is used to do a systematic error x-check.
#

s8 = files("system8/*.txt") \
     .restrict()
	 
# the topo are also known as the T&P ttbar analysis.
ttdilep_topo = files("topo_ttemu/*.txt") \
               .restrict()

# PDF are from Giacinto, who can't keep the names straight, which makes for a mess here.
ttbar_pdf_7_all = files("ttbar_pdf/*/*/*/*6bins.txt") \
                  .restrict() \
                  .filter(analyses = ["PDF_6bins_emu_2jets", "PDF_6bins_emu_3jets", \
									  "PDF_6bins_ll_2jets", "PDF_6bins_ll_3jets"])

ttbar_pdf_7_2j = ttbar_pdf_7_all \
                  .filter(analyses = ["PDF_6bins_ll_2jets", "PDF_6bins_emu_2jets"])

ttbar_pdf_7_3j = ttbar_pdf_7_all \
                  .filter(analyses = ["PDF_6bins_ll_3jets", "PDF_6bins_emu_3jets"])
				  


# Kinematic selection				  
ttbar_kinsel_3jet = files("ttbar_kinsel/*/*_em3j.txt") \
                    .restrict()

# We want the 2 jet results as well, but only where they don't overlap with
# Richard's inputs (ttdilep_topo).
ttbar_kinsel_2jet = files("ttbar_kinsel/*/*_em2j.txt") \
                    .restrict() \
                    .filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"])
				  
sources = s8 + ttdilep_topo + ttbar_pdf_7_all + ttbar_kinsel_3jet + ttbar_kinsel_2jet

#
# Build up the central dijet fits. "dijet" is our best estimate, in the end, of the dijet
# fits.
#

dijet = s8

# The file "commonbinning.txt" just contains some empty specifications that have the binning. They don't contain
# any real data. It should have the same binning as the D*. The _30 is without the 20-30 to deal with the PDF method,
# which has a bin we ignore from 25-30, and that bin can't really participate.
#

rebin_template_all = files("commonbinning.txt") \
    .filter(analyses=["rebin"])

rebin_template = rebin_template_all \
    .filter(ignore=[".*300-pt-500.*"])

rebin_template_30 = files("commonbinning.txt") \
    .filter(analyses=["rebin_30"]) \
    .filter(ignore=[".*300-pt-500.*"])
#
# We want several versions of the pdf fit to end up in the
# final file. This is for specialized use.
#

ttbar_pdf_7_combined = ttbar_pdf_7_all.bbb_fit("ttbar_PDF_7b")
ttbar_pdf_7_combined_2j = ttbar_pdf_7_2j.bbb_fit("ttbar_PDF_7b_2j")
ttbar_pdf_7_combined_3j = ttbar_pdf_7_3j.bbb_fit("ttbar_PDF_7b_3j")

#
# Do the ttbar results
# Several different fits are required, so this gets
# a bit complex, unfortunately.
#

# JVF05 is s8 + ttbar pdf. The s8 needs to be re-binned for this.
s8_pdf_rebin = (s8 + rebin_template_30).rebin("rebin_30", "<>_rebin")

ttbar_dijet_jvf05 = (\
		ttbar_pdf_7_all.filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"]) \
         + s8_pdf_rebin.filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"]) \
		).bbb_fit("combined_pdf_dijet")

ttbar_dijet_topo = (\
		s8.filter(jets=["AntiKt4TopoLCJVF0_5"]) \
		+ ttdilep_topo.filter(jets=["AntiKt4TopoLCJVF0_5"]) \
		+ ttbar_kinsel_3jet.filter(jets=["AntiKt4TopoLCJVF0_5"]) \
		).bbb_fit("ttbar_dijet_topo_ks")

ttbar_dijet_nojvf = (\
		s8.filter(jets=["AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"]) \
		+ ttbar_kinsel_3jet.filter(jets=["AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"]) \
		+ ttbar_kinsel_2jet.filter(jets=["AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"]) \
        ).bbb_fit("ttbar_dijet_nojvf")

# one ring to rule them all...
ttbar_fits_7 = ttbar_pdf_7_combined \
    + ttbar_pdf_7_combined_2j \
    + ttbar_pdf_7_combined_3j \
    + ttbar_dijet_jvf05 \
    + ttbar_dijet_topo

ttbar_fits_10 = ttbar_dijet_nojvf

ttbar_fits = ttbar_fits_7 + ttbar_fits_10

#
# Next, we need to build up the master fits that will be used to make charm and tau results.
# This requires re-binning to match the D* input bins (for both charm and tau, as they
# are just versions of each other).
#

ttbar_rebin = (rebin_template + ttbar_fits) \
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

dstar_template = (files("Dstar/*/JVF05/*.txt") + files("Dstar/*/noJVF/*.txt")) \
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

negative = (files("negative_tags/*/JVF05/*.txt") + files("negative_tags/*/noJVF/*.txt")) \
           .restrict()

light_sf = negative

sources += negative

####################################
# Plotting

#
# Extrapolate everything
#

mcCalib = files("MCcalib/*.txt") \
    .restrict() \
    .filter(ignore=[".*20-pt-30.*"])

rebin_template_high = rebin_template_all \
    .filter(ignore=[".*20-pt-30.*"])

mcCalib_rebin = (rebin_template_high + mcCalib) \
    .rebin("rebin", "<>_rebin")

default_extrapolated = (\
        dijet \
        + ttbar_fits_10 \
        + mcCalib \
        ) \
        .extrapolate("MCcalib")

rebin_extrapolated = (\
    charm_sf \
    + tau_sf \
    + mcCalib_rebin \
    + ttbar_fits_7
    ) \
    .extrapolate("MCcalib_rebin")

all_extrapolated = default_extrapolated + rebin_extrapolated

# Currently can't extrapolate:
#  neg tags - because they are split in eta, and the extrapolation isn't.

####################################
# The CDI file.
#

master_cdi_file = \
    light_sf \
    + all_extrapolated \
    + sources
defaultSFs = master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "MCefficiencies_for_CDI_2.2.2014.root")
master_cdi_file.plot("MC12-CDI")
master_cdi_file.plot("MC12-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
sources.dump(sysErrors = True, name="sources")

(master_cdi_file + defaultSFs).plot("MC12-ByTagger", byCalibEff = True, effOnly=True)

# Done!
