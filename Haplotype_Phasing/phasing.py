import time
import numpy as np
import sys
import copy 

def readFile(name, s = None, e = None):
    with open(name) as f:
        a = list()
        for line in f:
            b = line.split( )
            a.append(b[s:e])
        return np.transpose(a)


def readcols(a, start=None, end=None):
    b = list()
    if end == None or end > len(a[0]):
        end = len(a[0])
    for row in a:
        b.append(row[start:end])
    return b


def complementary(genotype, haplotype):
    length = len(genotype)
    comp = list()
    for i in np.arange(0,length):
        if genotype[i] == '*':
            comp.append(haplotype[i])
        else:
            comp.append(int(genotype[i]) - int(haplotype[i]))
    return comp

def gen(a):
    collection = {}
    probability = {}
    for geno in a:
        temphaplo = {}

        haplo = list()
        haplo.append(list())
        for pos in geno:
            if pos == '2':
                for h in haplo:
                    h.append(1)
            elif pos == '0':
                for h in haplo:
                    h.append(0)
            else:
                temp = copy.deepcopy(haplo)
                for h in haplo:
                    h.append(1)
                for h in temp:
                    h.append(0)
                haplo = haplo + temp

        while (len(haplo) > 0):
            q = [1,-1]
            a = haplo.pop()
            b = complementary(geno, a)
            if a == b:
                probability[' '.join(map(str,a))] = -1
                temphaplo[' '.join(map(str,a))] = [2,-1]
            else:
                haplo.remove(b)
                temphaplo[' '.join(map(str,a))] = [1,-1]
                temphaplo[' '.join(map(str,b))] = [1,-1]
                probability[' '.join(map(str,a))] = -1
                probability[' '.join(map(str,b))] = -1
                
        collection[' '.join(geno)] = temphaplo
    return collection, probability



def maximize(collection, probability, top = 30):
    z = 0
    while z < top:
        z = z+1

        for a in collection:
            haplo = collection[a]
            sumh = 0
            for h in haplo:
                val = haplo[h][0]*probability[h]
                haplo[h][1] = val
                sumh = sumh + val
            for o in haplo:
                haplo[o][1] = haplo[o][1]/ float(sumh)

        sump = 0
        for a in probability:
            tot = 0
            for g in collection:
                if a in collection[g]:
                    tot = tot + collection[g][a][1]
            probability[a] = tot
            sump = sump + tot
        
        for a in probability:
            probability[a] = probability[a] / float(sump) 
    return collection, probability


def init(a):

    collection, probability = gen(a)
    
    total = len(probability)
    for i in probability:
        probability[i] = 1.0/total

    collection, probability = maximize(collection, probability)
    
    key = {}
    master = a
    lines = len(master) 
    for k in np.arange(0,lines):
        m = master[k]
        a = " ".join(m)
        haplo = collection[a]
        for i in haplo:            
            j = complementary(m, i.split( ))
            haplo[i][0] = haplo[i][1]*haplo[' '.join(map(str,j))][1]
        one = max(haplo, key=haplo.get)
        two = complementary(m, one.split( ))
        key[k] = [[one, ' '.join(map(str,two))], a]
    return key


        
def main():
    
    infile = sys.argv[1]
    outfile = sys.argv[2]
    complete = readFile(infile)
    
    interval = 12
    complen = len(complete[0])
    l = 0
    
    fl = open(outfile, "w")
    while l < complen:
        a = readcols(complete, l, l+interval)
        key1 = init(a)
        
        b = list()
        siz = len(key1)
        for i in np.arange(0,siz):
            b.append(key1[i][0][1].split( ))
            b.append(key1[i][0][0].split( ))
        c = np.transpose(b)
        for i in c:
            fl.write(' '.join(i))
            fl.write('\n')
        l = l+interval
            
    fl.close()

main()
