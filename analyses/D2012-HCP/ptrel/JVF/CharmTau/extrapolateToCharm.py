
import os
import glob

for oldfile in glob.glob( os.path.join('./', '*_toGordon.txt') ):

    infile = open(oldfile,"r")
    line = infile.readline()
    if line.find(",bottom,")!=-1:
        print "copying file " + oldfile
        newfile = oldfile
        newfile = newfile.replace("_toGordon.txt","_charm_toGordon.txt")
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
            if line.find(",bottom,") != -1:
                line = line.replace(",bottom,",",charm,");
            if line.find("}") != -1:
                outfile.write('                sys(extrapolation from b to c,11%) \n');
            outfile.write(line)
        outfile.write('}\n')    
        
