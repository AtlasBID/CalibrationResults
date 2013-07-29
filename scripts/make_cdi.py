#
# Create the CDI file from the input files
#

from files import files
from comboFitCommands import dumpCommandResult, listToString, dumpFile, rerunCommand, dumpTitle
from FutureFile import FutureFile
import comboGlobals

import ROOT
import shutil

#
# The CDI operator.
#
def make_cdi (sfobj, name, defaults_file = None, eff_file = None, Check=True):
    rf = FutureFile()
    comboGlobals.Commands += [CDI(sfobj, name,
                                  files(defaults_file, no_files_ok = True),
                                  files(eff_file, no_files_ok = True),
                                  Check, rf)]
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
    # Plot a bunch of inputs with a certian name
    def __init__(self, sfinfo, name, defaults_file, ttbar, check, futurefile):
        self._sf = sfinfo
        self._name = name
        self._check = check
        self._ttbar = ttbar
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

        lfiles = files
        if self._defaults_file:
            lfiles += " %s" % listToString(self._defaults_file.ResolveToFiles(html))
            fList += self._defaults_file.ResolveToFiles(html)

        if self._ttbar:
            lfiles += " %s" % listToString(["--copy%s" % l for l in self._ttbar.ResolveToFiles(html)])
            fList += self._ttbar.ResolveToFiles(html)

        lfiles += " --restrictedMC"

        dumpTitle(html, title)
        if rerunCommand(fList, outFile, lfiles, html):
            errcode = dumpCommandResult(html, "FTConvertToCDI.exe %s" % lfiles, store=cmdLog)
            if errcode == 0:
                shutil.copy ("output.root", outFile)
            else:
                print >> html, "<b>CDI building failed with error code %s</b>" % errcode
                print >> html, "Command line arguments: %s" % files

        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Inputs have not changed, resuing results from last run</p>"

        if rerunCommand(fList, cmdCopyOut, lfiles, html):
            errcode = dumpCommandResult(html, "FTCopyDefaults.exe %s output %s" % (lfiles, cmdCopyOut), store=cmdLogCopy)
            if errcode <> 0:
                print >> html, "<b>Default building failed with error code %s</b>" % errcode
                print >> html, "Command line arguments: %s" % files

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
                errcode = dumpCommandResult(html, "FTCheckOutput.exe %s" % outFile, store=cmdLog)

            else:
                dumpFile(html, cmdLog)
                print >> html, "<p>Inputs have not changed, resuing results from last run</p>"
            
            dumpROOTFile(html, outFile)
