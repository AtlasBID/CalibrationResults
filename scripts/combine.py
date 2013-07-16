#!/bin/env python
#
# Start from nothing, build the output file, the combination, etc.
#
# Use a rather OO/fluent interface to run the fitting
#

import os
import sys
import comboGlobals

#
# Leader that will do the basics
#
def doCombo(name, cleanFilesFirst=False, zipResults=False):

    #
    # Get everythign setup for loading.
    #

    from files import files

    #
    # Load in the module. This will trigger the actual processing
    # as the commands are encountered in the file.
    #
    
    (n_dir, n_name) = os.path.split(name)
    if n_dir != "":
        sys.path = [n_dir] + sys.path
    (n_module, n_ext) = os.path.splitext(n_name)

    configInfo = __import__ (n_module)

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
    # doing the work is a matter of looping through the commands that have been
    # stored up.
    #

    for c in comboGlobals.Commands:
        c.Execute(html, configInfo)

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
        os.system("tar -czf %s-noplots.tar.gz --exclude='*plots*.root' --exclude='*.tar.gz' %s*" % (configInfo.name, configInfo.name))

#
# When invokation occurs from the command line.
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
    else:
        doCombo(args[0], cleanFilesFirst=options.clean, zipResults=options.zip)
