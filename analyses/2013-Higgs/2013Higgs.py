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
#MV1 60% JVF (EM, LC)
    ["MV1", "0.9867"], 
    ["MV1", "0.9827 "], 
#MV1 70%
    ["MV1", "0.8119"], 
    ["MV1", "0.7892"], 
#MV1 80%
    ["MV1", "0.3900"], 
    ["MV1", "0.3511"],
#MV1 85%
#    ["MV1", "0.1644"], 
    ["MV1", "0.1340"], 
#MV1c 60% JVF (EM)
    ["MV1c", "0.8353"],
#MV1c 70% JVF (EM)
    ["MV1c", "0.7028"], 
#MV1c 80% JVF (EM)
    ["MV1c", "0.4050"],    
#JetFitterCharm (EM, LC)
    ["JetFitterCharm", "-0.9_NONE"], 
    ["JetFitterCharm", "-0.9_0.95"],
    ["JetFitterCharm", "-0.9_2.5"]    
    ]

# And the filtering of the taggers mentioned above is done by
# adding a restrict function onto the default object. This is one of those
# very cool things about how python works.

sfObject.restrict = lambda self: self.filter(
    taggers=taggers,
    jets=["AntiKt4TopoEMJVF0_5", "AntiKt4TopoLCJVF0_5"],
    ignore=[".*25-pt-30.*",".*300-pt-400.*", ".*system8.*20-pt-30.*", ".*JetFitterCharm-.*AntiKt4TopoEM.*"]
    )

###############################
# Bottom inputs

# top

ttbar_pdf_7_all = files("ttbar_pdf/*/JVF05/*7bins.txt") \
                  .restrict() \
                  .filter(analyses =["ttbar_pdf_emu_2jets_7bins", "ttbar_pdf_emu_3jets_7bins", "ttbar_pdf_ll_2jets_7bins", "ttbar_pdf_ll_3jets_7bins", "PDF_dl_7bins_ll_2jets", "PDF_dl_7bins_ll_3jets", "PDF_dl_7bins_emu_2jets", "PDF_dl_7bins_emu_3jets"])

ttbar_pdf_7_2j = files("ttbar_pdf/*/JVF05/*7bins.txt") \
                 .restrict() \
                 .filter(analyses =["ttbar_pdf_emu_2jets_7bins", "ttbar_pdf_ll_2jets_7bins", "PDF_dl_7bins_ll_2jets", "PDF_dl_7bins_emu_2jets"])

ttbar_pdf_7_combined = ttbar_pdf_7_all.bbb_fit("ttbar_pdf_7_fit")

ttbar_pdf_7_combined_2j = ttbar_pdf_7_2j.bbb_fit("ttbar_pdf_7_2j_fit")

ttbar = ttbar_pdf_7_combined + ttbar_pdf_7_combined_2j

sources = ttbar_pdf_7_all + ttbar_pdf_7_2j

###############################
# Charm Inputs (taus derived from charm too)


rebin_template = files("commonbinning.txt") \
                 .filter(analyses=["rebin"])

ttbar_rebin = (rebin_template + ttbar) \
              .rebin("rebin", "<>_rebin")

dstar_template = files("Dstar/*/JVF05/*.txt") \
        .restrict()

charm_sf = (dstar_template + ttbar_rebin) \
           .dstar("DStar_<>", "DStar")

tau_sf = charm_sf.add_sys("extrapolation from charm", "22%", changeToFlavor="tau")

sources += dstar_template

###############################
# Light quark inputs

negative = files("negative_tags/*/JVF05/*.txt") \
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
defaultSFs = master_cdi_file.make_cdi("MC12-CDI", "defaults.txt", "MCefficiencies_for_CDI_18.12.2013.root")
master_cdi_file.plot("MC12-CDI")
master_cdi_file.plot("MC12-CDI-Tagger-Trends", effOnly=True, byTaggerEff=True)
master_cdi_file.dump(sysErrors = True, name="master")
master_cdi_file.dump(metadata = True, name="master-metadata")
sources.dump(sysErrors = True, name="sources")

###############################
# Plotting

(master_cdi_file + defaultSFs).plot("MC12-ByTagger", byCalibEff = True, effOnly=True)
