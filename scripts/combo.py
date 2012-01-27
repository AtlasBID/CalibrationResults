#!/bin/env python
#
# Start from mothing, build the output file, the combination, etc.
#
# Argument to this script is a "name" which is what we will use to
# actually do input files.
#

import os
import sys

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
    # Build the standard command line
    #

    stdCmdArgs = buildArgs(configInfo)

    #
    # Get a list of the names
    #

    result = os.system("FTDump.exe %s --names" % stdCmdArgs)

    #
    # First job is to "check" the file to make sure it is ok.
    #

    result = os.system("FTDump.exe %s --check" % stdCmdArgs)
    print result

#
# If this is invoked from the command line..
#

if __name__ == "__main__":
    doCombo("MV180")

