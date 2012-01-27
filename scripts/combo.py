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
def runProc(cmdline):
    args = cmdline.split()
    p = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    text = p.communicate()[0]
    errorcode = p.returncode

    return errorcode, text

#
# Dump out some html about how it went
#
def dumpResultSection (html, err, text, title):
    print >> html, "<h1>%s</h1>" % title
    print >> html, "<PRE>%s</PRE>" % text
    print >> html, "result code: %d" % err

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

    errcode, result = runProc("FTDump.exe %s --names" % stdCmdArgs)
    dumpResultSection (html, errcode, result, "All analyses to be processed")

    #
    # First job is to "check" the file to make sure it is ok.
    #

    errcode, result = runProc("FTDump.exe %s --check" % stdCmdArgs)
    dumpResultSection (html, errcode, result, "Bin Consistency Check")

    if errcode <> 0:
        print "consitancy check failed, stopping now..."
        return

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

