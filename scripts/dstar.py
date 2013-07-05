#
# Do the D* calculation (scaling template D* files to the final D* values).
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile
from FutureFile import FutureFile
import comboGlobals

#
# We need a template analysis and something to call it when we are done.
#

def dstar(sfObj, outputAnaPattern, dstarAnaName):
    rf = FutureFile()

    fc = DStar(sfObj, rf, outputAnaPattern, dstarAnaName)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the D* calculation
#

class DStar:
    def __init__ (self, sfinfo, futureFile, outputAnaPattern, dstarAnaName):
        self._sf = sfinfo
        self._dstar = dstarAnaName
        self._outputAna = outputAnaPattern
        self._ff = futureFile

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        files += ' outputAna "%s" DStarAna %s' % (self._outputAna, self._dstar)

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputFile = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputFile

        title = "Calculating D* from template %s" % self._dstar

        if rerunCommand(fList, outputFile, html):

            errcod = dumpCommandResult(html, "FTDStarCalc.exe %s" % files, title, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to calculate D*! Command line: %s" % files
                raise BaseException("Unable to calc D*")

        else:
            dumpFile(html, cmdLog, title)
            print >> html, "<p>D* calc previously run, and no inputs have been changed. Using results from last run.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputFile

        #
        # File used for later stages in the analysis.
        #
        
        self._ff.SetFName("%s" % outputFile)
