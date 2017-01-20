#
# Smooth the CDI file
#

from comboFitCommands import dumpCommandResult
import comboGlobals

import shutil

def make_smooth (sfobj, name, order, smoothing, ptbins):

    comboGlobals.Commands += [smooth(sfobj, name, order, smoothing, ptbins)]

class smooth:
    # Setup the CDI command, remember everything.
    def __init__(self, sfinfo, name, order, smoothing, ptbins):
        self._sf = sfinfo
        self._name = name
        self._order = order
        self._smoothing = smoothing
        self._ptbins = ptbins

    def Execute(self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)

        inputFile = "%s-%s.root" % (configInfo.name, self._name)
        cmdLog = "%s-%s-cmd-log.txt" % (configInfo.name, self._name)
        cmdLogCopy = "%s-%s-cmd-copy-log.txt" % (configInfo.name, self._name)
        cmdCopyOut = "%s-%s-defaults-sf.txt" % (configInfo.name, self._name)

        print >> html, "<p>Smoothing the CDI file</p>"
        print >> html, "Command line: RUN_SMOOTHING %s %s %s %s" % (inputFile, self._order, self._smoothing, self._ptbins)
        errcode = dumpCommandResult(html, "source ../NPandSmoothingTools/scripts/RUN_SMOOTHING.sh %s %s %s %s" % \
                                   (inputFile, self._order, self._smoothing, self._ptbins), store=cmdLog)
        if errcode == 0:
            output = inputFile[:-5]+"_order_"+self._order+"_smoothing_"+self._smoothing+"_ptbins_"+self._ptbins+".root"
            shutil.move (output, inputFile[:-5]+"_smooth.root")

