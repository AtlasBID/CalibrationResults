#
# Config file to run the 2014-Winter-7TeV fitting script
#
# run as first argument to combine script!

# Imports are key for anything else to get done.

from files import files
from sfObject import sfObject

title = "2014 Winter Results at 7 TeV"
description = "Final combination for the 7 TeV data"
name="2014-Winter-7TeV"

# What taggers and OP's are we looking at? This list is used to filter
# everything later on so we don't end up with extra stuff in the CDI that
# calibration analyses have supplied.

taggers = [
#MV1 60%
    ["MV1", "0.905363"],
#MV1 70%
    ["MV1", "0.601713"],
#MV1 75%
    ["MV1", "0.404219"],
#MV1 85%
    ["MV1", "0.0714225"],
    ]

# And the filtering of the taggers mentioned above is done by
# adding a restrict function onto the default object. This is one of those
# very cool things about how python works.

sfObject.restrict = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4Topo"],
    ignore=[".*25-pt-30.*"]
    )

###############################
#### Bottom inputs

# di-jet input - S8
s8 = files("system8/*.txt") \
     .restrict()

# di-jet input - pTrel
ptrel = files ("ptrel/*txt") \
        .restrict()

# top input - kinematic selection in di-lepton channel
ttbar_kinsel = files("ttbar_kinsel/*.txt") \
               .restrict()

# top input - PDF with different final states and 6 bins
ttbar_pdf_6_all = files("ttbar_pdf/6bins/*6bins.txt") \
                  .restrict() \
                  .filter(analyses =["ttbar_pdf_emu_2jets_6bins","ttbar_pdf_emu_3jets_6bins","ttbar_pdf_ll_2jets_6bins","ttbar_pdf_ll_3jets_6bins"])
ttbar_pdf_6_2j = ttbar_pdf_6_all \
                 .filter(analyses =["ttbar_pdf_emu_2jets_6bins","ttbar_pdf_ll_2jets_6bins"])
ttbar_pdf_6_3j = ttbar_pdf_6_all \
                 .filter(analyses =["ttbar_pdf_emu_3jets_6bins","ttbar_pdf_ll_3jets_6bins"])

# top input - PDF with different final states and 10 bins
ttbar_pdf_10_all = files("ttbar_pdf/10bins/*.txt") \
                  .restrict() \
                  .filter(analyses =["ttbar_pdf_emu_2jets","ttbar_pdf_emu_3jets","ttbar_pdf_ll_2jets","ttbar_pdf_ll_3jets"])
ttbar_pdf_10_2j = ttbar_pdf_10_all \
                 .filter(analyses =["ttbar_pdf_emu_2jets","ttbar_pdf_ll_2jets"])
ttbar_pdf_10_3j = ttbar_pdf_10_all \
                 .filter(analyses =["ttbar_pdf_emu_3jets","ttbar_pdf_ll_3jets"])

# defining sources
sources = ttbar_pdf_6_all + ttbar_pdf_10_all + ttbar_kinsel

# what we'll be considered the dijet inputs later on
dijet = s8 + ptrel

# rebin should have the same binning as D*
rebin_template_all = files("commonbinning.txt") \
                     .filter(analyses=["rebin"])
rebin_template = rebin_template_all \
                 .filter(ignore=[".*300-pt-500.*"])
rebin_template_30 = files("commonbinning.txt") \
                    .filter(analyses=["rebin_30"]) \
                    .filter(ignore=[".*300-pt-500.*"])

# various top-based combination using 6-bin inputs 
ttbar_pdf_6_combined = ttbar_pdf_6_all.bbb_fit("ttbar_PDF_6b")
ttbar_pdf_6_combined_2j = ttbar_pdf_6_2j.bbb_fit("ttbar_PDF_6b_2j")
ttbar_pdf_6_combined_3j = ttbar_pdf_6_3j.bbb_fit("ttbar_PDF_6b_3j")

# various top-based combination using 10-bin inputs 
ttbar_pdf_10_combined = ttbar_pdf_10_all.bbb_fit("ttbar_PDF_10b")
ttbar_pdf_10_combined_2j = ttbar_pdf_10_2j.bbb_fit("ttbar_PDF_10b_2j")
ttbar_pdf_10_combined_3j = ttbar_pdf_10_3j.bbb_fit("ttbar_PDF_10b_3j")

ttbar_pdf_combined = ttbar_pdf_6_combined + ttbar_pdf_6_combined_2j + ttbar_pdf_6_combined_3j \
	+ ttbar_pdf_10_combined + ttbar_pdf_10_combined_2j + ttbar_pdf_10_combined_3j

# di-jet combination
dijet_combined = dijet.bbb_fit("dijet", extraFiles=files("stat_correlation_inputs.txt"))

# ttbar kinematic selection + dijet combined together
ttbar_kinsel_dijet = (ttbar_kinsel + dijet).bbb_fit("ttbar_kinsel_dijet", extraFiles=files("stat_correlation_inputs.txt"))

# ttbar kinematic selection (l+jets), ttbar pdf (dilep), and dijet

ttbar_dijet = (ttbar_kinsel + dijet + ttbar_pdf_10_all).bbb_fit("ttbar_kinsel_pdf_dijet", extraFiles=files("stat_correlation_inputs.txt"))

# rebinned results used to make charm and tau results 
ttbar_rebin = (rebin_template + ttbar_pdf_10_combined + ttbar_dijet) \
              .rebin("rebin", "<>_rebin")
dijet_rebin = (rebin_template + dijet) \
              .rebin("rebin", "<>_rebin")



###############################
#### Charm Inputs (taus derived from charm too)

dstar_template = files("Dstar/*.txt") \
                 .restrict()

charm_sf_ttbar = (dstar_template + ttbar_rebin + dijet_rebin) \
                 .dstar("DStar_<>", "DStar")

charm_sf_dijet = (dstar_template + dijet_rebin) \
                 .dstar("DStar_<>", "DStar")

charm_sf = charm_sf_ttbar + charm_sf_dijet

tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources += dstar_template



###############################
#### Light quark inputs

negative = files("negative_tags/*.txt") \
           .restrict()

light_sf = negative

sources += negative


###############################
#### Put together the CDI

master_cdi_file = sources \
				  + dijet_combined \
				  + ttbar_kinsel_dijet \
				  + ttbar_pdf_combined \
				  + ttbar_dijet \
				  + dijet \
                  + charm_sf \
                  + tau_sf \
                  + light_sf
defaultSFs = master_cdi_file.make_cdi("MC11-CDI", "defaults.txt", "MCefficiencies_for_CDI_7TeV_23.2.2014.root")
master_cdi_file.plot("MC11-CDI")
master_cdi_file.plot("MC11-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
sources.dump(sysErrors = True, name="sources")
ttbar_pdf_combined.plot("ttbar_pdf", effOnly=True)
(ttbar_kinsel_dijet+ttbar_pdf_combined+ttbar_dijet).plot("ttbar_all", effOnly=True)

###############################
# Plotting

(master_cdi_file + defaultSFs).plot("MC11-ByTagger", byCalibEff = True, effOnly=True)
