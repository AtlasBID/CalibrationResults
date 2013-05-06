#
# Run a fit on the inputs. This is a new command that runs on the input files.
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile
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
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)
        files += " --combinedName %s" % self._fitAna

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputSFName = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName

        title = "Fitting to %s" % self._fitAna

        #
        # Next, see if we have done this command already
        #

        if rerunCommand(fList, outputSFName):

            cmdout = open("%s-cmd.txt" % baseOutputName, "w")
            print >>cmdout, files
            cmdout.close()
        
            errcod = dumpCommandResult(html, "FTCombine.exe %s" % files, title, store=cmdLog)
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

            dumpFile(html, cmdLog, title)
            print >> html, "<p>Dumping file from last run of combination and including those results in our calculations as"
            print >> html, "the inputs have not changed since last run.</p>"


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


