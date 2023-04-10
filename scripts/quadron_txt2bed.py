import sys

data = open(sys.argv[1], 'r')
data = data.readlines()

f = open(sys.argv[2],"w") 

adjust = 1 #adjust for quadron to bed conversion: bed file is zero-based
for i in range(0,len(data)):
    crit = data[i].split()
    if crit[0] == "DATA:" and crit[4] != "NA":
        start = int(crit[1])
        length = int(crit[3])
        f.write("chrX\t%i\t%i\t%.2f\t%s\t%i\n" %(start-adjust, length+start-adjust, float(crit[4]), crit[2], length))
