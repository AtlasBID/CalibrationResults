#
# Run a fit on the inputs. This is a new command that runs on the input files.
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
from FutureFile import FutureFile
import comboGlobals

import shutil
import os

# Called from sfObject, do the fitting
def fit (sfobj, outputName, binByBin = False):
    rf = FutureFile()
    fc = Fit(sfobj, outputName, binByBin, rf)
    comboGlobals.Commands += [fc]
    return rf


#
# Fit the input files
#
class Fit:
    def __init__ (self, sfinfo, outputAnaName, binByBin, futureFile):
        self._sf = sfinfo
        self._fitAna = outputAnaName
        self._bbb = binByBin
        self._ff = futureFile

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)
        files += " --combinedName %s" % self._fitAna

        if self._bbb:
            files += " --binbybin"

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputSFName = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName

        ftype = "profile"
        if self._bbb:
            ftype = "bin by bin"
        title = "Fitting to %s (%s)" % (self._fitAna, ftype)

        #
        # Next, see if we have done this command already
        #

        dumpTitle(html, title)
        if rerunCommand(fList, outputSFName, files, html):

            cmdout = open("%s-cmd.txt" % baseOutputName, "w")
            print >>cmdout, files
            cmdout.close()
        
            errcod = dumpCommandResult(html, "FTCombine.exe %s" % files, store=cmdLog)
            if errcod == 0:
                if not os.path.exists("combined.txt"):
                    errcode = -1000

            if errcod == 0:
                shutil.move("combined.txt", outputSFName)
            else:
                print >> html, "<b>Combination failed with error code %s</b><p>" % errcod
                print >> html, "Command line arguments: %s" % files
                print "The Combination failed"
                
        else:
            print >> html, "<p>Dumping file from last run of combination and including those results in our calculations as"
            print >> html, "the inputs have not changed since last run.</p>"

            dumpFile(html, cmdLog)


        #
        # Ok, regardless of having re-run, dump all the info.
        #

        self._ff.SetFName(outputSFName)
        print >> html, '<a href="%s">Scale Factor text file</a>' % outputSFName
        print >> html, '<a href="%s-cmd.txt">Command Line Args</a>' % baseOutputName

        if os.path.exists("output.root"):
            shutil.move("output.root", "%s-diagnostics.root" % baseOutputName)
            print >> html, '<a href="%s-diagnostics.root">Diagnostics root file</a>' % baseOutputName
        if os.path.exists("combined.dot"):
            shutil.move("combined.dot", "%s-combined.dot" % baseOutputName)
            print >> html, '<a href="%s-combined.dot">graphviz input file</a>' % baseOutputName
        print >> html, "<p>"


