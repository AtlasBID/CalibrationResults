#
# Config file to run the 2013 Higgs fitting script
#
# run as first argument to combine script!

# Imports are key for anything else to get done.

from files import files
from sfObject import sfObject

title = "2013 Higgs Results"
description = "based onf full 2012 data, and updated pdf filts in EM and LC jets"
name="2013-Higgs"

# What taggers and OP's are we looking at? This list is used to filter
# everything later on so we don't end up with extra stuff in the CDI that
# calibration analyses have supplied.

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

# And the filtering of the taggers mentioned above is done by
# adding a restrict function onto the default object. This is one of those
# very cool things about how python works.

sfObject.restrict = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5", "AntiKt4TopoEMnoJVF", "AntiKt4TopoLCnoJVF"],
    ignore=[".*25-pt-30.*",".*300-pt-400.*", ".*system8.*20-pt-30.*"]
    )

###############################
# Bottom inputs

# dijet

s8 = files("system8/*.txt") \
    .restrict()

dijet_sources = s8

# top

ttbar_pdf_all = files ("ttbar_pdf/*/JVF05/*7bins.txt") \
            .restrict()

ttbar_pdf_all_comb = ttbar_pdf_all.bbb_fit("PDF_all_fit", saveCHI2Fits=True)
ttbar = ttbar_pdf_all_comb.filter(analyses=["PDF_all_fit"])

# What from above should end up in the official CDI?

bottom = s8

###############################
# Charm Inputs (taus derived from charm too)

dstar_template = files("DStar/*/JVF05/*.txt") \
        .restrict()

charm_sf = (dstar_template) \
           .dstar("DStar_<>", "DStar")

tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

###############################
# Light quark inputs

negative = files("negative_tags/*/JVF05/*.txt") \
           .restrict()

light_sf = negative

###############################
# Do the extrapolation

#### Warning: filtering out the 20-30 bin is because the extrapolation
####          code can't yet handle extrapolation on both sides of an axis,
####          or one where the error gets smaller.
####          We will need to decide what to do about this.
mcCalib = files("MCcalib/*.txt") \
    .restrict() \
    .filter(ignore=[".*20-pt-30.*"])

extrapolated = (bottom+mcCalib).extrapolate("MCcalib")

###############################
# Put together the CDI

final_cdi_file = ttbar \
                 + charm_sf \
                 + tau_sf \
                 + light_sf

final_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "MCefficiencies_for_CDI_21.11.2013.root")
final_cdi_file.save("MC12-CDI-All-Inputs")

###############################
# Plotting

ttbar.plot("PDF_all_fit", effOnly=True)
