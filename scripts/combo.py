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

#
# Build the standard command line arguments to the FT guy given
# the config file.
#
def buildArgs(config):
    badfiles = ""
    for ignoreAna in config.ignore_analyses:
        badfiles += " --ignore %s" % ignoreAna

    cmdfile = "%s %s" % (config.inputs, badfiles)
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
def dumpCommandResult (html, cmdline, title, printtime=True):
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
    # Build the standard command line
    #

    stdCmdArgs = buildArgs(configInfo)

    #
    # Get a list of the names
    #

    errcode = dumpCommandResult (html, "FTDump.exe %s --names" % stdCmdArgs, "All analyses to be processed", printtime = False)

    #
    # First job is to "check" the file to make sure it is ok.
    #

    errcode = dumpCommandResult(html, "FTDump.exe %s --check" % stdCmdArgs, "Bin Consistency Check")

    if errcode <> 0:
        print "consitancy check failed, stopping now..."
        return

    #
    # Next, do the combination itself
    #

    if configInfo.runCombination:
        errcode = dumpCommandResult(html, "FTCombine.exe %s" % stdCmdArgs, "Combination")

        # Cache all the files we can for this run so they are easy to get at.
        shutil.copy("output.root", "%s-diagnostics.root" % configInfo.name )
        shutil.copy("combined.dot", "%s-combined.dot" % configInfo.name )
        shutil.copy("combined.txt", "%s-sf.txt" % configInfo.name )
    else:
        dumpResultSection(html, "Config file turned off running the combination", "Combination")

    print >> html, '<a href="%s-diagnostics.root">Diagnostics root file</a>' % configInfo.name
    print >> html, '<a href="%s-combined.dot">graphviz input file</a>' % configInfo.name
    print >> html, '<a href="%s-sf.txt">Scale Factor text file</a>' % configInfo.name
    
    combinedFilename = "%s-sf.txt" % configInfo.name
    if os.path.exists(combinedFilename):
        stdCmdArgs += " %s" % combinedFilename

    #
    # Generate plots for this guy
    #

    dumpCommandResult(html, "FTPlot.exe %s" % stdCmdArgs, "SF Plots")
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

    errcode = dumpCommandResult(html, "FTConvertToCDI.exe %s --update" % stdCmdArgs, "Convert to CDI")

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
    doCombo("MV160")

