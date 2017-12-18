# Conversion from TopoJets inputs to PFlowJets + TrackJets inputs (step by step)

Input files for the AntiKt4EMPFlowJets, AntiKt2PV0TrackJets and AntiKtVR30Rmax4Rmin02TrackJets algorithms are produced by converting the input files of the AntiKt4EMTopoJets. 

The process is automatised through the [converInputFiles.py](https://github.com/AtlasBID/CalibrationResults/blob/master/analyses/2017-21-13TeV/convertInputFiles.py). The script shoudl always be processed from `CalibrationResults/analyses/2017-21-13TeV/`. 

## Specificities for the conversion
### AntiKt4EMPFlowJets
AntiKt4EMTopoJets name in the Analysis line is replaced  by AntiKt4EMPFlowJets.

### AntiKt2PV0TrackJets and AntiKtVR30Rmax4Rmin02TrackJets 
The first step is to replace the name of the algorithm in the Analysis line.

The second step is to modify the lowest pt bin:

| Flavour | Old binning | New binning |
|:-------:|:-----------:|:-----------:|
| bottom  | 20 < pt < 30| 10 < pt < 30|
| charm   | 25 < pt < 40| 20 < pt < 40|
| light di-jets  | 20 < pt < 60| 10 < pt < 60|
| light Zjets  | 20 < pt < 40| 10 < pt < 40|

The third step is to add a CaloJet extrapolation systematic uncertainty:

| Flavour | sys(FT_EFF_CaloJet_extrap,X) |
|:-------:|:-----------:|
| bottom | 5% |
| charm | 20% |
| light | 40% |
 
