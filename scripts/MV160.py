#
# Config for doing the MV180 combination and file generation for dijets only.
#

title = "MV160 dijet Combination"
name = "MV160"

#
# Input arguments
#

inputs = "analyses/System8-MV160.txt analyses/ptrel-MV160.txt analyses/ptrel-JFITNN70.txt"
#inputs = "analyses/ptrel-JFITNN70.txt"
ignore_analyses = [
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:20-pt-30:0-abseta-2.5",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:20-pt-140:0-abseta-0.6",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:20-pt-140:0.6-abseta-1.2",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:20-pt-140:1.2-abseta-1.8",
    "pTrel-bottom-JetFitterCOMBNN-0.35-AntiKt4Topo:20-pt-140:1.8-abseta-2.5",
    "system8-bottom-MV1-0.905363-AntiKt4Topo:200-pt-250:0-abseta-2.5",
    "kinsel_ljets-bottom-SV0-0.50-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-SV0-0.50-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-SV0-0.50-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-SV0-0.50-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-SV0-0.50-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-SV0-0.50-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-JetProb-0.50-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-JetProb-0.50-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-JetProb-0.50-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-JetProb-0.50-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-JetProb-0.50-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-JetProb-0.50-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.60-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.60-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.60-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.60-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.60-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.60-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.70-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.70-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.70-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.70-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.70-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.70-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.80-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.80-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.80-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.80-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.80-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-IP3D+SV1-0.80-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.57-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.57-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.57-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.57-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.57-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.57-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.60-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.60-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.60-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.60-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.60-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.60-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.70-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.70-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.70-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.70-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.70-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.70-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.80-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.80-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.80-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.80-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.80-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-JetFitterCOMBNN-0.80-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.601713-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.601713-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.601713-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.601713-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.601713-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.601713-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.404219-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.404219-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.404219-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.404219-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.404219-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.404219-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.0714225-AntiKt4Topo:25-pt-30:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.0714225-AntiKt4Topo:30-pt-60:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.0714225-AntiKt4Topo:60-pt-90:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.0714225-AntiKt4Topo:90-pt-140:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.0714225-AntiKt4Topo:140-pt-200:0-abseta-2.5",
    "kinsel_ljets-bottom-MV1-0.0714225-AntiKt4Topo:200-pt-300:0-abseta-2.5",
    "pTrel-bottom-MV1-0.905363-AntiKt4Topo:20-pt-200:0-abseta-0.6",
    "pTrel-bottom-MV1-0.905363-AntiKt4Topo:20-pt-200:0.6-abseta-1.2",
    "pTrel-bottom-MV1-0.905363-AntiKt4Topo:20-pt-200:1.2-abseta-1.8",
    "pTrel-bottom-MV1-0.905363-AntiKt4Topo:20-pt-200:1.8-abseta-2.5",
    ]

#
# The root file that we start everythign with.
#

mcEffRootFile = "mceff/TopCalibrations_rel17_MC11b_Convert.root"
CDIFile = "rel17_MC11b.root"

#
# Should we avoid the combination?
#
runCombination = 0
