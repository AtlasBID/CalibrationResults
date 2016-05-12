#
# Create the CDI file from the input files
#

from files import files
from comboFitCommands import dumpCommandResult, listToString, dumpFile, rerunCommand, dumpTitle
from FutureFile import FutureFile
import comboGlobals

import ROOT
import shutil
import os
from sfObject import sfObject

#
# The CDI operator.
#
def make_cdi (sfobj, name, defaults_file = None, eff_file = None, wp_file = None, Check=True):
    rf = FutureFile()

    df = defaults_file
    if not isinstance(df, sfObject):
        df = files(df, no_files_ok = True)

    ef = eff_file
    if not isinstance(ef, sfObject):
        ef = files(ef, no_files_ok = True)

    wp = wp_file
    if not isinstance(wp, sfObject):
        wp = files(wp, no_files_ok = True)

    comboGlobals.Commands += [CDI(sfobj, name, df, ef, wp, Check, rf)]
    return rf

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
# Build the CDI, and run the check.
#
class CDI:
    # Setup the CDI command, remember everything.
    def __init__(self, sfinfo, name, defaults_file, ttbar, wp, check, futurefile):
        self._sf = sfinfo
        self._name = name
        self._check = check
        self._ttbar = ttbar
        self._wp = wp
        self._defaults_file = defaults_file
        self._rf = futurefile

    # Run the CDI maker
    def Execute(self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        outFile = "%s-%s.root" % (configInfo.name, self._name)
        cmdLog = "%s-%s-cmd-log.txt" % (configInfo.name, self._name)
        cmdLogCopy = "%s-%s-cmd-copy-log.txt" % (configInfo.name, self._name)
        cmdCopyOut = "%s-%s-defaults-sf.txt" % (configInfo.name, self._name)

        title = "Building CDI %s" % self._name

        versionInfo = "--config-info FileName %s" % outFile
        if "BuildNumber" in os.environ.keys():
            versionInfo += " --config-info BuildNumber %s" % os.environ["BuildNumber"]
        else:
            versionInfo += " --config-info BuildNumber Custom"

        lfiles = files
        if self._defaults_file:
            lfiles += " %s" % listToString(self._defaults_file.ResolveToFiles(html))
            fList += self._defaults_file.ResolveToFiles(html)

        if self._ttbar:
            lfiles += " %s" % listToString(["--copy%s" % l for l in self._ttbar.ResolveToFiles(html)])
            fList += self._ttbar.ResolveToFiles(html)

        if self._wp:
            lfiles += " %s" % listToString(["--copy%s" % l for l in self._wp.ResolveToFiles(html)])
            fList += self._wp.ResolveToFiles(html)

        dumpTitle(html, title)
        print >> html, "Command line arguments: %s" % files
        if rerunCommand(fList, outFile, lfiles, html):
            errcode = dumpCommandResult(html, "FTConvertToCDI %s %s" % (lfiles, versionInfo), store=cmdLog)
            if errcode == 0:
                shutil.copy ("output.root", outFile)
            else:
                print >> html, "<b>CDI building failed with error code %s</b>" % errcode

        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Inputs have not changed, resuing results from last run</p>"

        print >> html, "Command line arguments: %s" % files
        if rerunCommand(fList, cmdCopyOut, lfiles, html):
            errcode = dumpCommandResult(html, "FTCopyDefaults %s output %s" % (lfiles, cmdCopyOut), store=cmdLogCopy)
            if errcode <> 0:
                print >> html, "<b>Default building failed with error code %s</b>" % errcode

        else:
            dumpFile(html, cmdLogCopy)
            print >> html, "<p>Inputs have not changed, resuing results from last run</p>"

        print >> html, '<a href="%s">CDI File</a>' % outFile
        print >> html, '<a href="%s">Defaults</a>' % cmdCopyOut

        self._rf.SetFName(cmdCopyOut)

        cmdLog = "%s-%s-check-cmd-log.txt" % (configInfo.name, self._name)
        if self._check:
            print >> html, "<p>Running a check on the CDI file</p>"
            if rerunCommand(fList, cmdLog, outFile, html):
                errcode = dumpCommandResult(html, "FTCheckOutput %s" % outFile, store=cmdLog)

            else:
                dumpFile(html, cmdLog)
                print >> html, "<p>Inputs have not changed, resuing results from last run</p>"
            
            dumpROOTFile(html, outFile)
