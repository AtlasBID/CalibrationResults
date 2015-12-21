#
# Given two analyses, use the difference as a new systeamtic on the first analysis.
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
from FutureFile import FutureFile
import comboGlobals

def sys_delta_ana (sfObj, newAnaName, baseAnaName, deltaAnaName, sysName):
    rf = FutureFile()

    fc = DeltaAna(sfObj, rf, newAnaName, baseAnaName, deltaAnaName, sysName)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to do the delta of the analysis.
#

class DeltaAna:
    def __init__ (self, sfinfo, futureFile, newAnaName, baseAnaName, deltaAnaName, sysName):
        self._sf = sfinfo
        self._ff = futureFile
        self._newAna = newAnaName
        self._baseAna = baseAnaName
        self._deltaAna = deltaAnaName
        self._sys = sysName

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        files += ' outputAna "%s" calcRelDiff "%s" "%s" "%s"' % (self._newAna, self._baseAna, self._deltaAna, self._sys)

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputFile = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputFile

        title = "Calculating Relative Difference between %s and %s to create %s" % (self._baseAna, self._deltaAna, self._newAna)

        dumpTitle(html, title)
        if rerunCommand(fList, outputFile, files, html):

            errcod = dumpCommandResult(html, "FTManipSys %s" % files, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to calc new systematic error! Command line: %s" % files
                raise BaseException("Unable to calculate new systematic error")

        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Recalc previously run, and no inputs have been changed. Using results from last run.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputFile

        #
        # File used for later stages in the analysis.
        #
        
        self._ff.SetFName("%s" % outputFile)
