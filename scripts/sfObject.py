#
# Base class for a scale factor object. May contain more than one SF, but this
# base object doesn't know about it. The key thing is that once the list of inputs
# that this represents is "set", it can't be changed.
#

import comboGlobals
import comboCommandClasses

class sfObject:

    def __init__ (self):
        pass

    # We are to plot our inputs. Add ourselves to the list
    # of things to be plotted.
    
    def plot(self, name):
        comboGlobals.Commands += [comboCommandClasses.Plot(self, name)]
    
