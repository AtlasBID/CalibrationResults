#!/bin/env python
#
#  take joe's input file and make something "sensible" out of them.
#
#  Mask off bins at 60-75, 110-140, 140-200.
#

import os
import sys

def makefile (inputfile):
    f = open (inputfile, 'r')

    for line in f:
        items = line.rstrip().split(' ')
        tagger = items[0]
        op = items[4]

        ptlow = items[1]
        pthigh = items[2]
        etalow = "0.0"
        etahigh = "2.5"

        ptrelCut = items[5]

        if ptlow == "60" and pthigh == "75":
            continue
        if ptlow == "110" and pthigh == "140":
            continue
        if ptlow == "140" and pthigh == "200":
            continue

        if ptrelCut != "690.7":
            continue
        
        statCor = items[7];
        print "Correlation(pTrel, system8, bottom, %s, %s, AntiKt4Topo) {" % (tagger, op)
        print "  bin(%s<pt<%s,%s<abseta<%s) {" % (ptlow, pthigh, etalow, etahigh)
        print "    statistical(%s)" % statCor
        print "  }"
        print "}"

    f.close()
    

if __name__ == "__main__":
    makefile(sys.argv[1])
    
