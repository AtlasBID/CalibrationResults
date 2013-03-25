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

    def GetBaseConfig (self):
        return self._baseCommandLine

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
# Given a name, which may be a wildcard, see fi we can find it. First
# on its own, and then relative to everythign in the sys.path variable.
#
def pathglob (name):
    path_to_try = ["./"] + sys.path
    for p in path_to_try:
        flist = glob.glob(os.path.join(p, name))
        if len(flist) > 0:
            return flist

    print 'Input file path "%s" had no matching files' % name
    return []


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
        inputs = pathglob(config.inputs)
    else:
        flist = [f for fwild in config.inputs for f in pathglob(fwild)]
        found = False
        for f in flist:
            inputs += " %s" % f
            found = True
        if not found:
            raise "Unable to find any input files!"
            
    #
    # Build the commands out of that.
    #

    cmdfile = cmdSequences ("%s %s" % (inputs, badfiles))

    #
    # If the user wants, they may restrict the analyses that are looked
    # at (do to multiple combinations, for example). We need a complete
    # list of the flavors to fill in any missing gaps. However, to do that
    # we need to walk through all the input files (using FTDump, actually, to
    # get the listing).
    #

    analysisGroups = {}
    if "analysisGroupings" in config.__dict__:
        analysisGroups = config.analysisGroupings

    allAnalysisNames = getCommandResult("FTDump.exe %s --qnames" % cmdfile.GetFullConfig())
    try:
        listofflavors = list(set([l.split('//')[1] for l in allAnalysisNames]))
    except:
        print "Error parsing inputs:"
        print allAnalysisNames
        
    for f in listofflavors:
        if f not in analysisGroups:
            analysisGroups[f] = {'combined': []}

    #
    # For each tagger in the list, generate a command sequence. Things are
    # made a bit complex b/c the list of analysis groups applies to a single
    #

    for flavor in listofflavors:
        for g in config.DoOnlyTaggers:
            onlyFlagsBase = " --flavor %s" % flavor
            for anaGroup in analysisGroups[flavor]:
                onlyFlags = "%s --combinedName %s" % (onlyFlagsBase, anaGroup)
                if len(analysisGroups[flavor][anaGroup]) > 0:
                    for anaName in analysisGroups[flavor][anaGroup]:
                        onlyFlags += "  --analysis %s" % anaName
                
                if g["flavor"] == "*" or g["flavor"] == flavor:
                    if g["tagger"] != "*":
                        onlyFlags += " --tagger " + g["tagger"]
                    if g["op"] != "*":
                        onlyFlags += " --operatingPoint " + g["op"]
                    if g["jet"] != "*":
                        onlyFlags += " --jetAlgorithm " + g["jet"]

                cmdfile.addConfig (onlyFlags)
        
    return cmdfile

#
# Run a command line and return the data. Store to an output file if it is set.
#
def runProc(cmdline, output, printtime, store = None):
    args = cmdline.split()
    fout = None
    if store:
        fout = open(store, 'w')
        
    p = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.rstrip()
        if printtime:
            line = "%s   %s" % (time.asctime(), line)
        print >> output, line
        if store:
            print >> fout, line

    p.communicate()
    errorcode = p.returncode

    return errorcode

#
# Run a command, capture the output to a string. Strip off the &#&@ RooFit header
# if it is in there.
#
def getCommandResult (cmdline):
    args = cmdline.split()
        
    p = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    lines = []
    headerDone = False
    linecounter = 0
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.rstrip()
        if not headerDone:
            if len(line) == 0:
                continue
            if line.find("RooFit") >= 0:
                linecounter = 4
            if linecounter > 0:
                linecounter = linecounter - 1
                continue
            headerDone = True

        lines.append(line)

    p.communicate()

    return lines

#
# Run a command and dump the info in a section. Returns the process
# error code. We will add the "time" to the output if requested, and
# we can also tee the info to file 'store'
#
def dumpCommandResult (html, cmdline, title="", printtime=True, store = None):
    if title <> "":
        print >> html, "<h1>%s</h1>" % title
    print >> html, "<PRE>"
    err = runProc(cmdline, html, printtime, store)
    print >> html, "</PRE>"
    print >> html, "result code: %d" % err
    return err

#
# Dump out some html for a section
#
def dumpResultSection (html, text,  title):
    print >> html, "<h1>%s</h1>" % title
    print >> html, "<PRE>%s</PRE>" % text


#
# Dump out a file into the html in a <PRE> section.
#
def dumpFile (html, fname):
    f = open(fname, 'r')
    print >> html, "<PRE>"
    for l in f:
        print >> html, l.rstrip()
    print >> html, "</PRE>"

#
# Walk through a root tree and dump it out
#
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
    doConsistencyCheck = True
    if doConsistencyCheck:
        for cmd in stdCmdArgs:
            errcode = dumpCommandResult(html, "FTDump.exe %s --check" % cmd)
            if errcode <> 0:
                success = False
    else:
        print "** Warning - Bin Concistency Check Turned Off"
        
    if not success:
        print "consitancy check failed, stopping now..."
        return

    #
    # Figure out what types of combination we are going to run.
    #

    comboTypeInfo = [{"type" : "profile", "prefix" : ""}]
    if "CombinationTypeInfo" in configInfo.__dict__:
        comboTypeInfo = configInfo.CombinationTypeInfo

    #
    # Next, do the combination itself
    #

    print >> html, "<h1>Combination</h1>"

    for cmd in stdCmdArgs:
        for comboType in comboTypeInfo:
            cmd = cmd + " --%s" % comboType["type"]
            if len(comboType["prefix"]) > 0:
                cmd = cmd + " --prefix%s" % comboType["prefix"]
                
            baseOutputName = "%s-%s" % (configInfo.name, hash(cmd))
            combinedFilename = "%s-sf.txt" % baseOutputName
            cmdLog = "%s-cmb-log.txt" % baseOutputName
            cmdOpt = "%s-cmb-cmd.txt" % baseOutputName

            # Should we run the combo?
            dorun = True

            if not configInfo.runCombination:
                dorun = False

            if os.path.exists(combinedFilename):
                dorun = False
                    
            if not dorun:
                print >> html, "Not running the combination."
        
                if not os.path.exists(cmdLog):
                    print >> html, "<b>Log file is missing for this combination run! Delete %s to re-run</b>" % combinedFilename
                else:
                    print >> html, " Dumping file from last run of combination and including those results in later calculations."
                    dumpFile(html, cmdLog)

            else:
                # Cache the options for later use

                cout = open(cmdOpt, 'w')
                print >> cout, cmd
                cout.close()

                # Run the combo
        
                errcode = dumpCommandResult(html, "FTCombine.exe %s" % cmd, store=cmdLog)

                # If no output file appeared, then we also failed.
                if errcode == 0:
                    if not os.path.exists("combined.txt"):
                        errcode = -1000

                # Cache all the files we can for this run so they are easy to get at.
                if errcode == 0:
                    shutil.move("combined.txt", "%s-sf.txt" % baseOutputName )
                    if os.path.exists("output.root"):
                        shutil.move("output.root", "%s-diagnostics.root" % baseOutputName )
                        if os.path.exists("combined.dot"):
                            shutil.move("combined.dot", "%s-combined.dot" % baseOutputName )
                else:
                    print >> html, "<b>Combination failed with error code %s</b><p>" % errcode
                    print >> html, "Command line arguments: %s" % cmd
                    print "The Combination failed"

    
            # if we have an output file, include it in things we do below.
            if os.path.exists(combinedFilename):
                stdCmdArgs.addToStandard(combinedFilename)

                print >> html, '<a href="%s-diagnostics.root">Diagnostics root file</a>' % baseOutputName
                print >> html, '<a href="%s-combined.dot">graphviz input file</a>' % baseOutputName
                print >> html, '<a href="%s-sf.txt">Scale Factor text file</a>' % baseOutputName
                print >> html, '<a href="%s-cmb-cmd.txt">Command Line</a>' % baseOutputName
                print >> html, "<p>"

    #
    # Generate plots for everyone we've done.
    #

    dumpCommandResult(html, "FTPlot.exe %s" % stdCmdArgs.GetBaseConfig(), "SF Plots")
    shutil.copy ("plots.root", "%s-plots.root" % configInfo.name)
    print >> html, '<a href="%s-plots.root">Scale Factor Plots</a>' % configInfo.name

    #
    # We have to start with MC files that have the efficiencies in them.
    # We get the list of them here.
    #

    mcEffFiles = configInfo.mcEffRootFile
    if not isinstance(mcEffFiles, list):
        mcEffFiles = [mcEffFiles]
    mcEffFiles = [pathglob(f)[0] for f in mcEffFiles]
    mcEffFilesBad = [f for f in mcEffFiles if not os.path.exists(f)]
    mcEffFilesGood = [f for f in mcEffFiles if os.path.exists(f)]

    for f in mcEffFilesBad:
        print "Can't find root file %s" % f

    addF = ""
    for f in mcEffFilesGood:
        addF += "--copy%s " % f
        
    errcode = dumpCommandResult(html, "FTConvertToCDI.exe %s %s" % (stdCmdArgs.GetBaseConfig(), addF), "Convert to CDI")

    if errcode <> 0:
        print "Failed to build CDI"
        return

    outputROOT = configInfo.CDIFile
    shutil.copy ("output.root", outputROOT)
    print >> html, '<p><a href="%s">%s</a>' % (outputROOT, outputROOT)
        
    print >> html, "<h2>File Contents</h2>"
    dumpROOTFile(html, outputROOT)
    
    dumpCommandResult(html, "FTCheckOutput.exe %s" % outputROOT, "Output File Contents Check");

    # Finally, some info about when this was generated so it can be re-created.

    print >> html, "<h2>Package SVN Revision Information</h2>"
    dumpCommandResult(html, "pwd")
    dumpCommandResult(html, "svn info")
    dumpCommandResult(html, "svn status")
    
#
# Run the full thing
#
def doCombo(name, cleanFilesFirst=False, zipResults=False):
    #
    # load in the module for name so we can get all the config info
    # it will search sys.path for the module... If there is a directory
    # specified then add it to the search path, and if this is a file name
    # strip off the .py...
    #
    
    (n_dir, n_name) = os.path.split(name)
    if n_dir != "":
        sys.path = [n_dir] + sys.path
    (n_module, n_ext) = os.path.splitext(n_name)

    configInfo = __import__ (n_module)
    print configInfo.title

    #
    # Clean out any old results first
    #

    if cleanFilesFirst:
        print "  Removing results of previous run"
        [ os.remove(f) for f in os.listdir(".") if f.startswith(configInfo.name) ]

    #
    # Dump what happens to a html file as we go...
    #

    html = open("%s.html" % configInfo.name, "w")
    print >> html, "<html><header><title>%s</title></header><body>" % configInfo.title
    print >> html, "<h1>%s</h1>" % configInfo.title
    if configInfo.description:
        print >> html, "<p>%s</p>" % configInfo.description

    #
    # Do the work
    #

    doComboImpl(configInfo, html)

    #
    # Done with the log...
    #

    print >> html, "</body></html>"
    html.close()

    #
    # Zip up everything
    #

    if zipResults:
        os.system("tar -czf %s.tar.gz %s*" % (configInfo.name, configInfo.name))
        os.system("tar -czf %s-noplots.tar.gz --exclude='*plots.root' --exclude='*.tar.gz' %s*" % (configInfo.name, configInfo.name))

#
# If this is invoked from the command line..
#

if __name__ == "__main__":
    from optparse import OptionParser
    o = OptionParser()
    o.add_option("--clean", default=False, action="store_true")
    o.add_option("--zip", default=False, action="store_true")

    (options, args) = o.parse_args()

    if len(args) != 1:
        print "Usage: combo.py [flags] <config-name>"
        print "  --clean      Clean all result files first"
        print "  --zip        Generate a tar.gz file of all results"
        print "  config name must be in python's search path"
    doCombo(args[0], cleanFilesFirst=options.clean, zipResults=options.zip)
