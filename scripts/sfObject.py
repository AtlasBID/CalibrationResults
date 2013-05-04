#
# Base class for a scale factor object. May contain more than one SF, but this
# base object doesn't know about it. The key thing is that once the list of inputs
# that this represents is "set", it can't be changed.
#

class sfObject:

    def __init__ (self):
        pass

    # They are trying to do something (like plot or fit). See what we can do
    def __getattr__ (self, name):

        # See if we can find a python file called name.py
        m = __import__(name)
        if name in m.__dict__:
            f = lambda args: m.__dict__[name](self, args)
            return f
        else:
            raise AttributeError
    
    
    
