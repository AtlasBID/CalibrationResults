#
#  Rebin one analysis into another analysis
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
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
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        files += ' templateAna %s outputAna "%s"' % (self._template, self._ana)

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputFile = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputFile

        title = "Combining bins for %s (%s)" % (self._ana, self._template)

        dumpTitle(html, title)
        if rerunCommand(fList, outputFile, files, html):

            errcod = dumpCommandResult(html, "FTCombineBins %s" % files, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to rebin! Command line: %s" % files
                raise BaseException("Unable to rebin")

        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Rebin previously run, and no inputs have been changed. Using results from last run.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputFile

        #
        # File used for later stages in the analysis.
        #
        
        self._ff.SetFName("%s" % outputFile)
