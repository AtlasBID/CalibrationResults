#
# Save all the input files as a single output file. This is useful
# to just put it all in one nice location for later use.
#

#
# Do the D* calculation (scaling template D* files to the final D* values).
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
from FutureFile import FutureFile
import comboGlobals

#
# We need a template analysis and something to call it when we are done.
#

def save(sfObj, outputFName):
    rf = FutureFile()
    fc = SaveOutput(sfObj, outputFName, rf)
    comboGlobals.Commands += [fc]

    return rf

#
# Command object to actually save the file.
#

class SaveOutput:
    def __init__ (self, sfinfo, outputFileName, futurefile):
        self._sf = sfinfo
        self._outputName = outputFileName
        self._ff = futurefile

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        outputFile = "%s-%s.txt" % (configInfo.name, self._outputName)
        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        cmdLog = "%s-cmd-log.txt" % baseOutputName

        files += " --asInput output %s" % outputFile

        title = "Saving all files as %s" % outputFile

        dumpTitle(html, title)
        if rerunCommand(fList, self._outputName, files, html):

            errcod = dumpCommandResult(html, "FTDump.exe %s" % files, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to dump output files. Command line: %s" % files
                raise BaseException("Unable to dump SF's")

        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Dump previously run, and no inputs have been changed. Using results from last run.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % self._outputName

        self._ff.SetFName(outputFile)
