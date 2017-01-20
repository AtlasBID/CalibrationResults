#
# Build nuisance parameters in the CDI file
#

from comboFitCommands import dumpCommandResult
import comboGlobals

import shutil

def make_nuisance_parameters (sfobj, name):

    comboGlobals.Commands += [nuisance_parameters(sfobj, name)]

class nuisance_parameters:
    # Setup the CDI command, remember everything.
    def __init__(self, sfinfo, name):
        self._sf = sfinfo
        self._name = name

    def Execute(self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)

        inputFile = "%s-%s.root" % (configInfo.name, self._name)
        cmdLog = "%s-%s-cmd-log.txt" % (configInfo.name, self._name)
        cmdLogCopy = "%s-%s-cmd-copy-log.txt" % (configInfo.name, self._name)
        cmdCopyOut = "%s-%s-defaults-sf.txt" % (configInfo.name, self._name)

        print >> html, "<p>Nuisance parameters in the CDI file</p>"
        print >> html, "Command line: RUN_EIGEN_ANALYSIS %s %s %s %s" % (inputFile)
        errcode = dumpCommandResult(html, "source ../NPandSmoothingTools/scripts/RUN_EIGEN_ANALYSIS.sh %s" % \
                                   (inputFile), store=cmdLog)

