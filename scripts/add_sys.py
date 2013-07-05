#
# Add a systematic to an analysis (and rename it).
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile
from FutureFile import FutureFile
import comboGlobals

#
# We need a template analysis and something to call it when we are done.
#

def add_sys(sfObj, newSysName, newSysValue, changeToFlavor = None, outputAna = None):
    rf = FutureFile()

    fc = AddSys(sfObj, rf, outputAna, newSysName, newSysValue, changeToFlavor)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the rebinning.
#

class AddSys:
    def __init__ (self, sfinfo, futureFile, outputAna, newSysName, newSysValue, changeToFlavor):
        self._sf = sfinfo
        self._ff = futureFile
        self._outputAna = outputAna
        self._newSys = newSysName
        self._newSysValue = newSysValue
        self._newFlavor = changeToFlavor

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        files += ' addSysError "%s" %s' % (self._newSys, self._newSysValue)
        if self._newFlavor:
            files += " outputFlavor %s" % self._newFlavor
        if self._outputAna:
            files += " outputAna %s" % self._outputAna
            
        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputFile = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputFile

        title = "Adding systematic error %s" % self._newSys

        if rerunCommand(fList, outputFile, html):

            errcod = dumpCommandResult(html, "FTManipSys.exe %s" % files, title, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to add systematice error! Command line: %s" % files
                raise BaseException("Unable to add systematic error")

        else:
            dumpFile(html, cmdLog, title)
            print >> html, "<p>sys error previously run, and no inputs have been changed. Using results from last run.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputFile

        #
        # File used for later stages in the analysis.
        #
        
        self._ff.SetFName("%s" % outputFile)
