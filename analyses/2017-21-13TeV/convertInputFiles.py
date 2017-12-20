# Script to convert AntiKt4EMTopoJets to AntiKt2PV0TrackJets, AntiKtVR30Rmax4Rmin02TrackJets, AntiKt4EMPFlowJets by applying custom modifications to each files

import glob, os.path
import re
# Define extensions to be added to the name

extended = ['pflowjets', 'trackjets', 'VRtrackjets']

# CaloJetsExtrap
FT_EFF_CaloJet_Extrap = {'bottom' : '5%', 'charm' : '20%', 'light' : '40%'}
binning = { 'bottom' : ['bin(20<pt<30,0<abseta<2.5)','bin(10<pt<30,0<abseta<2.5)'],  
            'charm'  : ['bin(25<pt<40,0<abseta<2.5)', 'bin(20<pt<40,0<abseta<2.5)'],
            'light'  : ['bin(20<pt', 'bin(10<pt'],
        }
# Function to find the flavour wihtin the analysis
def findFlavour(inputString):
    ret = ''
    if 'bottom' in inputString:
        ret = 'bottom'
    elif 'charm' in inputString:
        ret = 'charm'
    elif 'light' in inputString:
        ret = 'light'
    return ret

# Custom modifications to the files written using replace()
# All the modification should be defined here
# Special attention is required while modifying the files, e.g. be sure that the occurence is unique or specify more patterns

def applyPFlowJets(inputString):
    output = inputString.replace('AntiKt4EMTopoJets','AntiKt4EMPFlowJets')
    return output

def applyTrackJets(inputString):
    flav = findFlavour(inputString)
    output = inputString.replace('AntiKt4EMTopoJets','AntiKt2PV0TrackJets')
    # change first binning from 20 to 10
    output = output.replace(binning[flav][0],binning[flav][1]) 
    # Add sys(FT_EFF_CaloJet_extrap,5%) after central_value
    CaloJetExtrap = "sys(FT_EFF_CaloJet_extrap,%s)"%FT_EFF_CaloJet_Extrap[flav]
    expressions = list(set(re.findall('central\_value\(\d+\.?\d*\%?,\d+\.?\d*\%?\)',inputString))) # set used to make sure replace is unique
    for exp in expressions:
        output = output.replace(exp,exp + '\n\t\t' + CaloJetExtrap) 
    return output

def applyVRTrackJets(inputString):
    flav = findFlavour(inputString)
    output = inputString.replace('AntiKt4EMTopoJets','AntiKtVR30Rmax4Rmin02TrackJets')
    output = output.replace(binning[flav][0],binning[flav][1])
    # Add sys(FT_EFF_CaloJet_extrap,5%) after central_value
    CaloJetExtrap = 'sys(FT_EFF_CaloJet_extrap,%s)'%FT_EFF_CaloJet_Extrap[flav]
    expressions = list(set(re.findall('central\_value\(\d+\.?\d*\%?,\d+\.?\d*\%?\)',inputString))) # set used to make sure replace is unique
    for exp in expressions:
        output = output.replace(exp,exp + '\n\t\t' + CaloJetExtrap) 
    return output

# Compute cross-checks

def crosscheck(inputString, reference):
    ret = True
    truth = open(reference,'r').read()
    if truth == inputString:
        print "OK: reference %s matches input string"%reference
        ret = True
    else:
        print "Test failed for reference %s"%reference
        truthList = truth.split('\n')
        inputList = inputString.split('\n')
        print "Testing the length of non-matching files: %d reference, %d input, match:"%(len(truthList),len(inputList)),len(truthList)==len(inputList)
        print "Testing line by line (avoid artifacts, e.g. white space or end of file backline)"
        for i in range(0,len(inputList)):
            if truthList[i] != inputList[i]:
                print "Truth:",truthList[i]
                print "Conversion:",inputList[i]
                ret = False
        print "Result of line by line testing, match : ",ret
    return ret

def checkAll(pflowjets,trackjets,VRtrackjets):
    passedTest = 0
    print "Testing the routines to convert TopoJets inputs to PFlowsJets, TrackJets and VRTrackJets"
    print "Testing PFlowJets:"
    if crosscheck(pflowjets,"pflowjets.txt"): 
        passedTest += 1
    if crosscheck(trackjets,'trackjets.txt'):
        passedTest += 1
    if crosscheck(VRtrackjets,'VRtrackjets.txt'):
        passedTest += 1
    print "Number of matching tests passed : %d / 3 "%passedTest

# Convert the files

#for f in glob.glob("*jets/*/*.txt"): # Fetch all the files in the directory
for f in glob.glob("extrap/*/*.txt"): # Fetch all the files in the directory
    if not any(extension in f for extension in extended): # Read only the TopoJets we base our conversion on

        namePFlowJets = f.replace('.txt','_' + 'pflowjets'  + '.txt')
        nameTrackJets = f.replace('.txt','_' + 'trackjets'  + '.txt')
        nameVRTrackJets = f.replace('.txt','_' + 'VRtrackjets' + '.txt')


        TopoJets = open(f,'r').read() 
        print "Writing converted files"
        if not os.path.isfile(namePFlowJets):
            PFlowJets = applyPFlowJets(TopoJets) # Custom rules for different type of jets
            with open(namePFlowJets, 'w') as pflow:
                pflow.write(PFlowJets)
                pflow.close()
        if not os.path.isfile(nameTrackJets):
            TrackJets = applyTrackJets(TopoJets)
            with open(nameTrackJets, 'w') as tjets:
                tjets.write(TrackJets)
                tjets.close()
        if not os.path.isfile(nameVRTrackJets):
            VRTrackJets = applyVRTrackJets(TopoJets)
            with open(nameVRTrackJets, 'w') as vrjets:
                vrjets.write(VRTrackJets)
                vrjets.close()

        

