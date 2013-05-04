#
#  Rebin one analysis into another analysis
#

from comboFitCommands import dumpCommandResult, listToString
from FutureFile import FutureFile
import comboGlobals

#
# We need a template analysis and something to call it when we are done.
#

def rebin(sfObj, templateAnaName, rebinnedAnaName):
    rf = FutureFile()

    fc = Rebin(sfObj, rf, templateAnaName, rebinnedAnaName)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the rebinning.
#

class Rebin:
    def __init__ (self, sfinfo, futureFile, templateName, anaName):
        self._sf = sfinfo
        self._template = templateName
        self._ana = anaName
        self._ff = futureFile

    def Execute (self, html, configInfo):
        files = listToString(self._sf.ResolveToFiles(html))

        files += " templateAna %s outputAna %s" % (self._template, self._ana)

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        files += " output %s-sf.txt" % baseOutputName

        errcod = dumpCommandResult(html, "FTCombineBins.exe %s" % files, "Combining bins for %s" % self._ana)
        if errcod != 0:
            print >> html, "Failed to rebin! Command line: %s" % files
            raise BaseException("Unable to rebin")

        self._ff.SetFName("%s-sf.txt" % baseOutputName)
