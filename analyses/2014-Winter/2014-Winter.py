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
name = "2014-Winter-8TeV"
description = "Winter 2014 results, based on the full 2012 8 TeV data"

#
# Legal taggers. These will be used lower down to filter out the inputs to make sure
# we are dealing only with what we want to deal with.
#

taggers = [
#MV1 50% JVF (EM, LC)
    ["MV1", "0.992515446"], 
    ["MV1", "0.993981"], 
#MV1 60% JVF (EM, LC)
    ["MV1", "0.9867"], 
    ["MV1", "0.9827"], 
#MV1 70% JVF (EM, LC)
    ["MV1", "0.8119"], 
    ["MV1", "0.7892"], 
#MV1 80% JVF (EM, LC)
    ["MV1", "0.3900"], 
    ["MV1", "0.3511"],
#MV1 85% JVF (EM, LC)
    ["MV1", "0.1644"],
    ["MV1", "0.1340"],    
#MV1c 50% JVF (EM, LC)
    ["MV1c", "0.9237"], 
    ["MV1c", "0.9195"], 
#MV1c 57% JVF (EM, LC)
    ["MV1c", "0.8674"], 
    ["MV1c", "0.8641"],
#MV1c 60%, JVF (EM, LC)
    ["MV1c", "0.8353"], 
#MV1c 70%
    ["MV1c", "0.7028"], 
    ["MV1c", "0.7068"],
#MV1c 80%
    ["MV1c", "0.4050"], 
    ["MV1c", "0.4051"],
#JetFitterCharm Medium
	["JetFitterCharm", "-0.9_0.95"],
#JetFitterCharm Loose
	["JetFitterCharm", "-0.9_NONE"]
    ]

#
# We are only looking at the following (a nice way to add a function onto an object!):
#

sfObject.restrict_good = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"],
    ).verify_OPs("8TeV")

sfObject.restrict_ignore = lambda self: self.filter(
    ignore=[".*15-pt-20.*",".*25-pt-30.*",".*300-pt-400.*", ".*system8.*20-pt-30.*", ".*MV1-0.1340-AntiKt4TopoLCnoJVF.*", ".*MV1c-0.8353-AntiKt4TopoEMnoJVF.*", ".*0.1644-AntiKt4TopoEMnoJVF.*"]
    )
	
sfObject.restrict = lambda self: self.restrict_good().restrict_ignore()
	
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
ttbar_pdf_7_all = (files("ttbar_pdf/EM/*/*/*6bins.txt") + files("ttbar_pdf/LC/*/*/*7bins.txt")) \
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
				  					
ttbar_pdf_10_all = (files("ttbar_pdf/EM/*/10PT*/*jets.txt") + files("ttbar_pdf/LC/*/10PT*/*jets.txt")) \
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

# Kinematic selection				  
ttbar_kinsel_3jet = files("ttbar_kinsel/*/*_em3j.txt") \
                    .restrict()

# We want the 2 jet results as well, but only where they don't overlap with
# Richard's inputs (ttdilep_topo).
ttbar_kinsel_2jet_all = files("ttbar_kinsel/*/*_em2j.txt") \
                        .restrict()
ttbar_kinsel_2jet = ttbar_kinsel_2jet_all \
                    .filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"])
				  
sources_7  = ttbar_pdf_7_all
sources_10 = s8 + ttdilep_topo + ttbar_pdf_10_all + ttbar_kinsel_3jet + ttbar_kinsel_2jet_all


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
                 .filter(ignore=[".*300-pt-500.*", ".*500-pt-800.*", ".*800-pt-1200.*", ".*1200-pt-2000.*"])

rebin_template_30 = files("commonbinning.txt") \
                    .filter(analyses=["rebin_30"]) \
                    .filter(ignore=[".*300-pt-500.*", ".*500-pt-800.*", ".*800-pt-1200.*", ".*1200-pt-2000.*"])

#
# We want several versions of the pdf fit to end up in the
# final file. This is for specialized use.
#

ttbar_pdf_7_combined = ttbar_pdf_7_all.bbb_fit("ttbar_PDF_7b")
ttbar_pdf_7_combined_2j = ttbar_pdf_7_2j.bbb_fit("ttbar_PDF_7b_2j")
ttbar_pdf_7_combined_3j = ttbar_pdf_7_3j.bbb_fit("ttbar_PDF_7b_3j")

ttbar_pdf_10_combined = ttbar_pdf_10_all.bbb_fit("ttbar_PDF_10b")
ttbar_pdf_10_combined_2j = ttbar_pdf_10_2j.bbb_fit("ttbar_PDF_10b_2j")
ttbar_pdf_10_combined_3j = ttbar_pdf_10_3j.bbb_fit("ttbar_PDF_10b_3j")

#
# Do the ttbar results
# Several different fits are required, so this gets
# a bit complex, unfortunately.
#

# JVF05 is s8 + ttbar pdf. The s8 needs to be re-binned for this.
s8_pdf_rebin = (s8 + rebin_template_30).rebin("rebin_30", "<>_rebin")

ttbar_dijet_jvf05_7 = (\
		ttbar_pdf_7_all.filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"]) \
                + s8_pdf_rebin.filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"]) \
		).bbb_fit("combined_pdf_dijet_7")

ttbar_dijet_jvf05_10 = (\
		ttbar_pdf_10_all.filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"]) \
                + s8.filter(jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"]) \
		).bbb_fit("combined_pdf_dijet_10")

ttbar_dijet_topo = (\
		s8.filter(jets=["AntiKt4TopoLCJVF0_5"]) \
		+ ttdilep_topo.filter(jets=["AntiKt4TopoLCJVF0_5"]) \
		+ ttbar_kinsel_3jet.filter(jets=["AntiKt4TopoLCJVF0_5"]) \
		).bbb_fit("ttbar_dijet_topo_ks")
		
ttbar_dijet_ks = (\
		s8 \
		+ ttbar_kinsel_3jet \
		+ ttbar_kinsel_2jet_all \
		).bbb_fit("ttbar_dijet_ks")
		
ttbar_ks = (\
		ttbar_kinsel_3jet \
		+ ttbar_kinsel_2jet_all \
		).bbb_fit("KinSel_dilep")

# one ring to rule them all...
ttbar_fits_7 = ttbar_pdf_7_combined \
    + ttbar_pdf_7_combined_2j \
    + ttbar_pdf_7_combined_3j \
    + ttbar_dijet_jvf05_7

ttbar_fits_10 = \
	ttbar_dijet_topo \
	+ ttbar_dijet_ks \
	+ ttbar_ks \
	+ ttbar_pdf_10_combined \
	+ ttbar_pdf_10_combined_2j \
	+ ttbar_pdf_10_combined_3j \
    + ttbar_dijet_jvf05_10
	

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
			  
dijet_rebin = (dstar_rebin_template + dijet) \
			  .rebin("DStar", "<>_rebin")
              
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

charm_sf_dijet = (dstar_template + dijet_rebin) \
                 .dstar("DStar_<>", "DStar")
                 
charm_sf = charm_sf_ttbar + charm_sf_dijet
                 
tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources_4 = dstar_template

####################################
# Light SF come from the negative tags
#

negative = (files("negative_tags/*/JVF05/*.txt") + files("negative_tags/*/noJVF/*.txt")) \
           .restrict()

light_sf = negative

# We'd like to do this, but we can't extrapolate accross bin boundaries.
#sources_10 += negative

####################################
# Extrapolate everything
#

mcCalib = (files("MCcalib/SfPtB*.txt") + files("MCcalib/SfPtC*.txt") + files("MCcalib/SfPtT*.txt") + files("MCcalib/EtaBins/SfPtL*.txt")) \
    .restrict_good() \
    .filter(ignore=[".*20-pt-30.*"])

rebin_template_high = rebin_template_all \
    .filter(ignore=[".*20-pt-30.*"])

mcCalib_rebin = (rebin_template_high + mcCalib) \
    .rebin("rebin", "<>_rebin")

rebin_for_extrap_dstar = files("commonbinning.txt") \
                       .filter(analyses=["rebin_dstar"])

mcCalib_rebin_dstar = (rebin_for_extrap_dstar + mcCalib) \
    .rebin("rebin_dstar", "<>_rebin")

default_extrapolated = (\
        dijet \
        + ttbar_fits_10 \
        + mcCalib \
		+ sources_10
        ) \
        .extrapolate("MCcalib")

#	+ light_sf \
rebin_extrapolated = (\
    mcCalib_rebin \
    + ttbar_fits_7 \
	+ sources_7 \
    ) \
    .extrapolate("MCcalib_rebin")
	
rebin_dstar_extrapolated = (\
    charm_sf \
    + tau_sf \
    + mcCalib_rebin_dstar \
	) \
	.extrapolate("MCcalib_rebin")

all_extrapolated = default_extrapolated + rebin_extrapolated + rebin_dstar_extrapolated

# Currently can't extrapolate:
#  neg tags - because they are split in eta, and the extrapolation isn't.

####################################
# The CDI file.
#

master_cdi_file = \
    all_extrapolated \
	+ light_sf
defaultSFs = master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "StandardTag_8TeV_ttbar_140613151009.root")
master_cdi_file.plot("MC12-CDI")
master_cdi_file.plot("MC12-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
(sources_7+sources_10+sources_4).dump(sysErrors = True, name="sources")

#(master_cdi_file + defaultSFs).plot("MC12-ByTagger", byCalibEff = True, effOnly=True)

####################################
# Rebinned inputs for the continuous tagging
#
#rebin_for_cont = files("continuousbinning.txt")

#(charm_sf + tau_sf + rebin_for_cont).rebin("rebin_cont", "<>_continuous")

# Done!
