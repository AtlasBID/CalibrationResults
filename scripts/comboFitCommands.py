#
# methods, etc, to help with running command lines and sending the output
# to our log files
#

import subprocess
import time
import shutil
import os

#
# Convert a list of strings into a single string
#
def listToString (list):
    cmd = ""
    if list == None:
        return cmd
    
    for l in list:
        cmd += " " + str(l)
    return cmd

#
# Check the list of input file dates against the output file dates. If the inputs are
# more recent, then we must run again!
#
def rerunCommand (inputFiles, outputFile):
    if not os.path.exists(outputFile):
        return True

    mod_output = os.stat(outputFile).st_mtime

    for f in inputFiles:
        if not os.path.exists(f):
            raise BaseException("Input file %s does not exist. Not possible!" % f)
        if os.stat(f).st_mtime > mod_output:
            return True

    return False

#
# Run a command line and return the data. Store to an output file if it is set.
#
def runProc(cmdline, output, printtime, store = None, printoutput = True):
    args = cmdline.split()
    fout = None
    if store:
        fout = open(store, 'w')
        
    p = subprocess.Popen(cmdline, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.rstrip()
        if printtime:
            line = "%s   %s" % (time.asctime(), line)
        if printoutput:
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
def dumpCommandResult (html, cmdline, title="", printtime=True, store = None, printoutput=True):
    if title <> "":
        print >> html, "<h1>%s</h1>" % title
    print >> html, "<PRE>"
    err = runProc(cmdline, html, printtime, store, printoutput)
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
def dumpFile (html, fname, title=""):
    if len(title) > 0:
        print >> html, "<h1>%s</h1>" % title

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
