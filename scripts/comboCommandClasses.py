#
# Commands to be executed
#

from comboFitCommands import dumpCommandResult, listToString

import shutil

class Plot:
    # Plot a bunch of inputs with a certian name
    def __init__(self, sfinfo, name):
        self._sf = sfinfo
        self._name = name

    # Run the plotter!
    def Execute(self, html, configInfo):
        files = listToString(self._sf.ResolveToFiles(html))

        dumpCommandResult(html, "FTPlot.exe %s" % files, "Plots for %s" % self._name)
        shutil.copy ("plots.root", "%s-plots-%s.root" % (configInfo.name, self._name))
        print >> html, '<a href="%s-plots-%s.root">Scale Factor Plots</a>' % (configInfo.name, self._name)

        
