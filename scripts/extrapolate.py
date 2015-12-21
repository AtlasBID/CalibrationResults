#
# Apply an analysis that has relative scaling to a input
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
from FutureFile import FutureFile
import comboGlobals

#
# We need a template analysis and something to call it when we are done.
# The extrapAnaNames can be either an array or a single string.
# The extrapolations are taken as normal analyses, in the list of input files.
# None of the extrapolation analyses will find their way to the output.
#

def extrapolate(sfObj, extrapAnaNames):
    # Convert the list of extrap analysis names into 
    extraps = extrapAnaNames
    if not isinstance(extraps, (tuple, list,)):
        extraps = [extrapAnaNames]

    # Place holder for storing the results
    rf = FutureFile()

    fc = Extrapolate(sfObj, rf, extraps)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the extrapolation calculation
#

class Extrapolate:
    def __init__ (self, sfinfo, futureFile, mcAnaNames):
        self._sf = sfinfo
        self._ff = futureFile
        self._extraps = mcAnaNames

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputFile = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " --output %s" % outputFile

        anaListFlat = ""
        for name in self._extraps:
            if len(anaListFlat) > 0:
                anaListFlat += ", "
            anaListFlat += name
            files += " --extrapolation %s" % name

        title = "Extrapolating analyses from from %s" % anaListFlat

        dumpTitle(html, title)
        if rerunCommand(fList, outputFile, files, html):

            errcod = dumpCommandResult(html, "FTExtrapolateAnalyses %s" % files, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to extrapolate! Command line: %s" % files
                raise BaseException("Unable to extrapolate")

        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Extrapolation previously run, and no inputs have been changed. Using results from last run.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputFile

        #
        # File used for later stages in the analysis.
        #
        
        self._ff.SetFName("%s" % outputFile)
