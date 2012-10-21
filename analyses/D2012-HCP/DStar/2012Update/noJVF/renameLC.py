
import os
import glob

for oldfile in glob.glob( os.path.join('./', '*.txt') ):

    infile = open(oldfile,"r")
    line = infile.readline()

    print "copying file " + oldfile
    newfile = oldfile
    newfile = newfile.replace(".txt","_LC.txt")
    print "          to " + newfile
    
#open files
    outfile = open(newfile, "w")
    infile.seek(0);

#inquire numebr of lines
    count_lines = len(infile.readlines())
    
#put back pointer at the top
    infile.seek(0)

# stop when we found two consecutive }
    found = -1
    stop  = -1
    for i in range(count_lines):
        line = infile.readline()
        if found == 1:
            if line.find("}") != -1:
                stop = i
        if line.find("}") != -1:
            found = 1 
        else:
            found = 0

#put back pointer at the top
    infile.seek(0)

#finally create new files
    for i in range(stop):
        line = infile.readline()
        if line.find(",AntiKt4Topo") != -1:
            line = line.replace(",AntiKt4Topo",",AntiKt4TopoLC");
        outfile.write(line)
    outfile.write('}\n')    
        
