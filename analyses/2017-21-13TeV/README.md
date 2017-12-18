# Conversion from TopoJets inputs to PFlowJets + TrackJets inputs (step by step)

Input files for the AntiKt4EMPFlowJets, AntiKt2PV0TrackJets and AntiKtVR30Rmax4Rmin02TrackJets algorithms are produced by converting the input files of the AntiKt4EMTopoJets. 

The process is automatised through the [converInputFiles.py](https://github.com/AtlasBID/CalibrationResults/blob/master/analyses/2017-21-13TeV/convertInputFiles.py). The script should always be processed from `CalibrationResults/analyses/2017-21-13TeV/`. 

## Usage
To run the conversion, simply execute the following commands:

```bash
cd CalibrationResults/analyses/2017-21-13TeV/
python convertInputFiles.py
``` 

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
 
## Details of the implementation
The conversion is done via the [converInputFiles.py](https://github.com/AtlasBID/CalibrationResults/blob/master/analyses/2017-21-13TeV/convertInputFiles.py) script.
1. Fetch the TopoJets files in the repertories `bjets/ttbar_pdf/`, `cjets/ttbarC/` and `ljets/negative_tags/`.
2. Build the converted file names by adding the suffix `pflowjets`, `trackjets` and `VRtrackjets`.
3. Buff each TopoJets files into a string.
4. If the new converted files names don't exist, then apply the custom modifications via the respective functions, e.g. `applyPFlowJets`, write the new files with the new name in the same repertory as the TopoJets files.

One can implement any new modifications to apply during the conversation by adding or removing custom selection in the three functions: `applyPFlowJets`, `applyTrackJets` and `applyVRTrackJets`. 

To be noted: for the two different TrackJets, the systematic uncertainty is added after the line `central_value`. This line is found using regular expressions defined in the various `apply...` functions. 
