#!/bin/env python
#
# Start from mothing, build the output file, the combination, etc.
#
# Argument to this script is a "name" which is what we will use to
# actually do input files.
#

import os
import sys
import subprocess
import shutil
import ROOT
import time
import glob

#
# Build the standard command line arguments to the FT guy given
# the config file. Since we can have several iterations, we need
# to have some sort of class which can deal with this stuff.
#
class cmdSequences:
    def __init__ (self, cmdline):
        self._baseCommandLine = cmdline
        self._configs = []

    def addConfig (self, extraCmd):
        self._configs.append(extraCmd)

    def addToStandard (self, s):
        self._baseCommandLine += " %s" % s

    def GetNumberConfig (self):
        return len(self._configs)

    def GetConfig(self, index):
        return "%s %s" % (self._baseCommandLine, self._configs[index])

    def GetFullConfig (self):
        cmd = self._baseCommandLine
        for c in self._configs:
            cmd += " " + c
        return cmd

    class cmdSequenceItr:
        def __init__ (self, seq):
            self._seq = seq;
            self._index = 0

        def __iter__ (self):
            return self;

        def next(self):
            if self._index >= self._seq.GetNumberConfig():
                if self._index == 0:
                    self._index += 1
                    return self._seq.GetFullConfig()

                raise StopIteration

            self._index += 1
            return self._seq.GetConfig(self._index-1)

    def __iter__ (self):
        return cmdSequences.cmdSequenceItr(self)

#
# Create the configs for this run from the command line.
#
def buildArgs(config):
    badfiles = ""
    for ignoreAna in config.ignore_analyses:
        badfiles += " --ignore %s" % ignoreAna

    #
    # Do wild-card expansion
    #

    inputs = ""
    if isinstance(config.inputs, str):
        inputs = config.inputs
    else:
        flist = [f for fwild in config.inputs for f in glob.glob(fwild)]
        for f in flist:
            inputs += " %s" % f
            
    #
    # Build the commands out of that.
    #

    cmdfile = cmdSequences ("%s %s" % (inputs, badfiles))

    for g in config.DoOnlyTaggers:
        onlyFlags = ""
        if g["flavor"] != "*":
            onlyFlags += " --flavor " + g["flavor"]
        if g["tagger"] != "*":
            onlyFlags += " --tagger " + g["tagger"]
        if g["op"] != "*":
            onlyFlags += " --operatingPoint " + g["op"]
        if g["jet"] != "*":
            onlyFlags += " --jetAlgorithm " + g["jet"]

        cmdfile.addConfig (onlyFlags)
        
    return cmdfile

#
# Run a command line and return the data
#
def runProc(cmdline, output, printtime):
    args = cmdline.split()
    p = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        if printtime:
            print >> output, "%s   %s" % (time.asctime(), line.rstrip())
        else:
            print >> output, line.rstrip()

    p.communicate()
    errorcode = p.returncode

    return errorcode

#
# Run a command and dump the info in a section. Returns the process
# error code
#
def dumpCommandResult (html, cmdline, title="", printtime=True):
    if title <> "":
        print >> html, "<h1>%s</h1>" % title
    print >> html, "<PRE>"
    err = runProc(cmdline, html, printtime)
    print >> html, "</PRE>"
    print >> html, "result code: %d" % err
    return err

#
# Dump out some html for a section
#
def dumpResultSection (html, text,  title):
    print >> html, "<h1>%s</h1>" % title
    print >> html, "<PRE>%s</PRE>" % text


def dumpROOTDir (html, dir, indent):
    for k in dir.GetListOfKeys():
        c = ROOT.TClass.GetClass(k.GetClassName())
        isdir = c.InheritsFrom("TDirectory")
        if isdir:
            print >> html, "%s<b>%s</b>" % (indent, k.GetName())
            dumpROOTDir(html, k.ReadObj(), "%s  " % indent)
        else:
            print >> html, "%s<b>%s</b> - <i>%s</i>" % (indent, k.GetName(), k.GetClassName())
#
# Dump out the directory contents of a root file
# so that one can see what is going on in the ROOT file.
#
def dumpROOTFile (html, fname):
    f = ROOT.TFile(fname, "READ")
    print >> html, "<PRE>"
    print >> html, "%s" % fname
    dumpROOTDir (html, f, "  ")
    f.Close()
    print >> html, "</PRE>"

#
# Do the actual combo and root file building here
#
def doComboImpl (configInfo, html):
    
    #
    # Build the standard command line argument object.
    #

    stdCmdArgs = buildArgs(configInfo)

    #
    # Get a list of the names
    #

    errcode = dumpCommandResult (html, "FTDump.exe %s --names" % stdCmdArgs.GetFullConfig(), "All analyses to be processed", printtime = False)

    #
    # First job is to "check" the file to make sure it is ok.
    #

    print >> html, "<h1>Bin Consistency Check</h1>"

    success = True
    for cmd in stdCmdArgs:
        errcode = dumpCommandResult(html, "FTDump.exe %s --check" % cmd)
        if errcode <> 0:
            success = False

    if not success:
        print "consitancy check failed, stopping now..."
        return

    #
    # Next, do the combination itself
    #

    print >> html, "<h1>Combination</h1>"

    for cmd in stdCmdArgs:
        baseOutputName = "%s-%s" % (configInfo.name, hash(cmd))
        combinedFilename = "%s-sf.txt" % configInfo.name

        # Should we run the combo?
        dorun = True

        if not configInfo.runCombination:
            dorun = False

        if os.path.exists(combinedFilename):
            dorun = False

        if not dorun:
            dumpResultSection(html, "Config file turned off running the combination", "Combination")

        else:
            # Run the combo
        
            errcode = dumpCommandResult(html, "FTCombine.exe %s" % cmd)

            # Cache all the files we can for this run so they are easy to get at.
            if errcode == 0:
                shutil.copy("output.root", "%s-diagnostics.root" % baseOutputName )
                shutil.copy("combined.dot", "%s-combined.dot" % baseOutputName )
                shutil.copy("combined.txt", "%s-sf.txt" % baseOutputName )

                print >> html, '<a href="%s-diagnostics.root">Diagnostics root file</a>' % baseOutputName
                print >> html, '<a href="%s-combined.dot">graphviz input file</a>' % baseOutputName
                print >> html, '<a href="%s-sf.txt">Scale Factor text file</a>' % baseOutputName
            else:
                print "The Combination failed"

    
        # if we have an output file, include it in things we do below.
        if os.path.exists(combinedFilename):
            stdCmdArgs.addToStandard(combinedFilename)

    #
    # Generate plots for everyone we've done.
    #

    dumpCommandResult(html, "FTPlot.exe %s" % stdCmdArgs.GetFullConfig(), "SF Plots")
    shutil.copy ("plots.root", "%s-plots.root" % configInfo.name)
    print >> html, '<a href="%s-plots.root">Scale Factor Plots</a>' % configInfo.name

    #
    # We are going to copy the root file over and build it with
    # everything that is needed in it.
    #

    if not os.path.exists(configInfo.mcEffRootFile):
        print "Can't find root file %s" % configInfo.mcEffRootFile
    outputROOT = configInfo.CDIFile
    shutil.copy (configInfo.mcEffRootFile, "output.root")

    errcode = dumpCommandResult(html, "FTConvertToCDI.exe %s --update" % stdCmdArgs.GetFullConfig(), "Convert to CDI")

    if errcode <> 0:
        print "Failed to build CDI"
        return

    shutil.copy ("output.root", outputROOT)
    print >> html, '<p><a href="%s">%s</a>' % (outputROOT, outputROOT)
        
    print >> html, "<h2>File Contents</h2>"
    dumpROOTFile(html, outputROOT)
    
#
# Run the full thing
#
def doCombo(name):
    #
    # load in the module for name so we can get all the config info
    # it will search sys.path for the module...
    #
    
    configInfo = __import__ (name)
    print configInfo.title

    #
    # Dump what happens to a html file as we go...
    #

    html = open("%s.html" % name, "w")
    print >> html, "<html><header><title>%s</title></header><body>" % configInfo.title

    #
    # Do the work
    #

    doComboImpl(configInfo, html)

    #
    # Done with the log...
    #

    print >> html, "</body></html>"

#
# If this is invoked from the command line..
#

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage: combo.py <config-name>"
        print "  config name must be in python's search path"
    doCombo(sys.argv[1])

