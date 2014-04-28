#
# Verify the operating points in the input files using FTDump's check functionality.
#
# You could use the dump command directly, but this just tries to make it a little easier.
#

#
# We need only the year that we should be doing the check agains: "7TeV" or "8TeV", for example.
# Passed in as a string or a number!
#
def verify_OPs (f, year):

    #
    # First, do both fits
    #

    f.dump(cnames="../Combination/inputdata/FTCrossCheckInput-%s.txt" % year)
    return f
