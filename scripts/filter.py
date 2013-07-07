#
# Filter the input for some set of criteria.
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
from FutureFile import FutureFile
import comboGlobals

#
# We will filter out input files on some criteria
#

def filter(sfObj, analyses = [], taggers=[], ignore=[], jets=[]):
    if len(analyses) == 0 and len(taggers) == 0 and len(ignore) == 0 and len(jets) == 0:
        print "Filtering nothing. Will pass everythign on"
        return sfObj
    
    rf = FutureFile()
    fc = Filter(sfObj, analyses, taggers, ignore, jets, rf)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the filter.
#

class Filter:
    def __init__ (self, sfinfo, analyses, taggers, ignore, jets, futureFile):
        self._sf = sfinfo
        self._anas = analyses
        self._taggers = taggers
        self._ignore = ignore
        self._ff = futureFile
        self._jets = jets

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        for a in self._anas:
            files += " --analysis %s" % a

        for t in self._taggers:
            files += " --tagger %s --operatingPoint %s" % (t[0], t[1])

        for i in self._ignore:
            files += " --ignore '%s'" % i

        for j in self._jets:
            files += " --jetAlgorithm %s" % j

        files += " --asInput"

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputName = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputName

        title = "Filtering for %s" % listToString(self._anas + self._taggers + self._ignore + self._jets)

        dumpTitle(html, title)
        print >> html, "<b>Command line: FTDump.exe %s</b>" % files
        if rerunCommand(fList, outputName, files, html):
            errcod = dumpCommandResult(html, "FTDump.exe %s" % files, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to filter! Command line: %s" % files
                raise BaseException("Unable to filter")

        else:
            print >> html, "<p>Using results of last filter command as no inputs have changed.</p>"
            dumpFile(html, cmdLog)

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputName
        
        self._ff.SetFName(outputName)
