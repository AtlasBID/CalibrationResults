#
# Run a fit on the inputs. This is a new command that runs on the input files.
#

from comboFitCommands import dumpCommandResult, listToString
from FutureFile import FutureFile
import comboGlobals

import shutil
import os

# Called from sfObject, do the fitting
def fit (sfobj, outputName):
    rf = FutureFile()
    fc = Fit(sfobj, outputName, rf)
    comboGlobals.Commands += [fc]
    return rf


#
# Fit the input files
#
class Fit:
    def __init__ (self, sfinfo, outputAnaName, futureFile):
        self._sf = sfinfo
        self._fitAna = outputAnaName
        self._ff = futureFile

    def Execute (self, html, configInfo):
        files = listToString(self._sf.ResolveToFiles(html))
        files += " --combinedName %s" % self._fitAna

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))

        cmdout = open("%s-cmd.txt" % baseOutputName, "w")
        print >>cmdout, files
        cmdout.close()
        
        errcod = dumpCommandResult(html, "FTCombine.exe %s" % files, "Fitting to %s" % self._fitAna)
        if errcod == 0:
            if not os.path.exists("combined.txt"):
                errcode = -1000

        if errcod == 0:
            shutil.move("combined.txt", "%s-sf.txt" % baseOutputName)
            self._ff.SetFName("%s-sf.txt" % baseOutputName)
            print >> html, '<a href="%s-sf.txt">Scale Factor text file</a>' % baseOutputName
            print >> html, '<a href="%s-cmd.txt">Command Line Args</a>' % baseOutputName

            if os.path.exists("output.root"):
                shutil.move("output.root", "%s-diagnostics.root" % baseOutputName)
                print >> html, '<a href="%s-diagnostics.root">Diagnostics root file</a>' % baseOutputName
            if os.path.exists("combined.dot"):
                shutil.move("combined.dot", "%s-combined.dot" % baseOutputName)
                print >> html, '<a href="%s-combined.dot">graphviz input file</a>' % baseOutputName
            print >> html, "<p>"

        else:
            print >> html, "<b>Combination failed with error code %s</b><p>" % errcode
            print >> html, "Command line arguments: %s" % files
            print "The Combination failed"

