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
# Check to see if command line options have changed.
#
def rerunCheckCommandLine (commandLine, outputFile):
    cmd_options = "%s-cmdopt.txt" % outputFile
    cmd_options_exists = os.path.exists(cmd_options)

    cmd_line = ""
    if cmd_options_exists:
        cmd_opt_in = file(cmd_options, "r")
        cmd_line = cmd_opt.readlines()[0].strip()
        cmd_opt_in.close()

    cmd_opt_good = cmd_line != commandLine

    if not cmd_opt_good:
        cmd_opt_out = file(cmd_options, "w")
        print >> cmd_opt_out, commandLine
        cmd_opt_out.close()

    return cmd_opt_good

#
# Check the dates of the input files.
#
def rerunCheckFileList(inputFiles, outputFile, html):

    out_infile_list = "%s-infiles.txt" % outputFile
    out_infile_list_exists = os.path.exists(out_infile_list)

    #
    # Read in the old list, and write out the new one so we are ready
    # for the next go-around
    #

    lst = []
    if out_infile_list_exists:
        lin = file(out_infile_list, "r")
        lst = [l.strip() for l in lin.readlines()]
        lin.close()
    
    lin = file(out_infile_list, "w")
    for f in inputFiles:
        print >> lin, f
    lin.close()
        
    # If the output file doesn't exist, then we really don't care about doing date
    # checks!

    if not os.path.exists(outputFile):
        return False
    
    mod_output = os.stat(outputFile).st_mtime

    # Compare each file to see if we used it previously or if
    # if it was in the list.
    
    isgood = True
    for f in inputFiles:
        if not os.path.exists(f):
            raise BaseException("Input file %s does not exist. Not possible!" % f)
        
        if not (f in lst):
            if html:
                print >> html, "<p>File '%s' is a never seen before input file." % f
        
        if os.stat(f).st_mtime > mod_output:
            if html:
                print >> html, "<p>File '%s' is newer than the output file" % f
            isgood = False

    return isgood


#
# Check the list of input file dates against the output file dates. If the inputs are
# more recent, then we must run again! Also, x-check the command line to see if any options
# have changed!
#
def rerunCommand (inputFiles, outputFile, commandLine, html = None):

    cmd_opt_good = rerunCheckCommandLine(commandLine, outputFile)
    file_list_good = rerunCheckFileList(inputFiles, outputFile, html)
    output_exists = os.path.exists(outputFile)

    # If any failures, then delete the output file to make sure we have to rerun.

    if cmd_opt_good and file_list_good and output_exists:
        return False

    if output_exists:
        os.unlink(outputFile)

    if html:
        if not output_exists:
            print >> html, "<p>Rerunning command because no previous output files exists</p>"
        if not file_list_good:
            print >> html, "<p>Rerunning command because of updates to the input file list.</p>"
        if not cmd_opt_good:
            print >> html, "<p>Rerunning command because of changes to the command line options.</p>"

    return True

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
# Dump out just a title.
#
def dumpTitle (html, title):
    print >> html, "<h1>%s</h1>" % title

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
