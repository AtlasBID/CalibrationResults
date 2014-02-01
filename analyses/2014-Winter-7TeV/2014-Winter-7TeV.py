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
    )

###############################
# Bottom inputs

# top

ttbar_pdf_6_all = files("ttbar_pdf/6bins/*6bins.txt") \
                  .restrict() \
                  .filter(analyses =["ttbar_pdf_emu_2jets_6bins","ttbar_pdf_emu_3jets_6bins","ttbar_pdf_ll_2jets_6bins","ttbar_pdf_ll_3jets_6bins"])

ttbar_kinsel = files("ttbar_kinsel/*.txt") \
               .restrict()

ttbar_pdf_6_all = ttbar_pdf_6_all.bbb_fit("ttbar_pdf_6_all_fit")

ttbar = (ttbar_pdf_6_all+ttbar_kinsel).bbb_fit("ttbar_pdf_6_all_fit")

sources = ttbar

###############################
# Charm Inputs (taus derived from charm too)

dstar_template = files("Dstar/*.txt") \
                 .restrict()

charm_sf = (dstar_template + ttbar) \
           .dstar("DStar_<>", "DStar")

tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources += dstar_template

###############################
# Light quark inputs

negative = files("negative_tags/*.txt") \
           .restrict()

light_sf = negative

sources += negative

###############################
# Do the extrapolation

#### Warning: filtering out the 20-30 bin is because the extrapolation
####          code can't yet handle extrapolation on both sides of an axis,
####          or one where the error gets smaller.
####          We will need to decide what to do about this.
#mcCalib = files("MCcalib/*.txt") \
#    .restrict() \
#    .filter(ignore=[".*20-pt-30.*"])

#extrapolated = (bottom+mcCalib).extrapolate("MCcalib")

###############################
# Put together the CDI

master_cdi_file = ttbar \
                 + charm_sf \
                 + tau_sf \
                 + light_sf \
                 + sources
defaultSFs = master_cdi_file.make_cdi("MC11-CDI", "defaults.txt", "MCefficiencies_for_CDI_16.1.2014_test.root")
master_cdi_file.plot("MC11-CDI")
master_cdi_file.plot("MC11-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
sources.dump(sysErrors = True, name="sources")

###############################
# Plotting

(master_cdi_file + defaultSFs).plot("MC11-ByTagger", byCalibEff = True, effOnly=True)
