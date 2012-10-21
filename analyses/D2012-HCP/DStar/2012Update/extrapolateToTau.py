
import os
import glob

for oldfile in glob.glob( os.path.join('./', '*.txt') ):

    infile = open(oldfile,"r")
    line = infile.readline()
    if line.find(",charm,")!=-1:
        print "copying file " + oldfile
        newfile = oldfile
        newfile = newfile.replace(".txt","_tau.txt")
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
            if line.find(",charm,") != -1:
                line = line.replace(",charm,",",tau,");
            if line.find("}") != -1:
                outfile.write('     sys(extrapolation from charm,22%) \n');
            outfile.write(line)
        outfile.write('}\n')    
        
