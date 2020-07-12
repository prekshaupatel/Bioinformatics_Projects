import numpy as np
from Bio import SeqIO
import sys
########################################################
########### GENERATING FEATURES ########################
def complist(n):
    p = ['A','C','G','T']
    comp = list()
    comp.append("")
    i = 0
    while i < n:
        i = i+1
        temp = list()
        for a in p:
            for b in comp:
                temp.append(b+a)
        comp = temp

    sym = set()
    t = n
    if n%2 == 0:
        n = int(n/2)
        for a in comp:
            if a[:n] == a[n:]:
                sym.add(a)
    n = t
    if n%3 == 0:
        n = int(n/3)
        for a in comp:
            if a[:n] ==	a[n:2*n] and a[:n] == a[2*n:]:
                sym.add(a)
    for j in sym:
        comp.remove(j)

    return comp
    
def percentACGT(line, n, complete_list): #n is size of substring
    comp = complete_list
    i = 0
    stop = len(line)+1-n
    temp = {}
    for a in comp:
        temp[a] = 0
        
    while i < stop:
        a = line[i:i+n]
        i = i+1
        if a in temp:
            temp[a] = temp[a] + 1


    for a in temp:
        temp[a] = temp[a]*len(a)/float(i)

    return temp

def lenACGT(line, n, complete_list): #n is size of substring
    comp = complete_list
    i = 0
    stop = len(line)+1-n
    temp = {}
    for a in comp:
        temp[a] = 0
        
    while i < stop:
        a = line[i:i+n]
        i = i+1
        if a in temp:
            temp[a] = temp[a] + 1


    for a in temp:
        temp[a] = temp[a]*len(a)

    return temp




def avgACGT(line, n, complete_list): #n is size of substring
    comp = complete_list
    i = 0
    stop = len(line)+1-n
    temp = {}
    for a in comp:
        i = 0
        cnt = 0
        maxl = 0
        while i < stop:
            if line[i:i+n] == a:
                j = 1
                while i+n < stop:
                    i = i+n
                    if line[i:i+n] != a:
                        break
                    j = j+1
                maxl = maxl + j
                cnt = cnt + 1
                
            i = i+1
        if(cnt == 0):
            temp[a] = 0
        else:
            temp[a] = maxl/float(cnt)
    #could change temp[a] = log(total+1),total*len(a)
    return temp

def longManualACGT(line, complete_list): #n is size of substring
    comp = complete_list
    i = 0
    stop = len(line)+1
    temp = {}
    for a in comp:
        n=len(a)
        stop = stop-n
        i = 0
        maxl = 0
        while i < stop:
            if line[i:i+n] == a:
                j = 1
                while i+n < stop:
                    i = i+n
                    if line[i:i+n] != a:
                        break
                    j = j+1
                maxl = maxl + j
            i = i+1
        temp[a] = maxl
    return temp


def rightWeightedACGT(line,n,complete_list):
    comp = complete_list
    i = 0
    stop = len(line)+1-n
    temp = {}
    for a in comp:
        i = 0
        total = 0
        while i < stop:
            if line[i:i+n] == a:
                begin = i+1
                j = 1
                while i+n < stop:
                    i = i+n
                    if line[i:i+n] != a:
                        break
                    j = j+1
                total = total + j*(begin)
            i = i+1    
        temp[a] = (total)*n
    #could change temp[a] = log(total+1),total*len(a)
    return temp

def leftWeightedACGT(line,n,complete_list):
    comp = complete_list
    i = 0
    stop = len(line)+1-n
    temp = {}
    for a in comp:
        i = 0
        total = 0
        while i < stop:
            if line[i:i+n] == a:
                end = stop-i+1
                j = 1
                while i+n < stop:
                    i = i+n
                    if line[i:i+n] != a:
                        break
                    j = j+1
                total = total + j*(end)
            i = i+1    
        temp[a] = (total)*n
    #could change temp[a] = log(total+1),total*len(a)
    return temp

def contACGT(line,n,complete_list):
    comp = complete_list
    i = 0
    stop = len(line)+1-n
    temp = {}
    for a in comp:
        i = 0
        total = 0
        while i < stop:
            if line[i:i+n] == a:
                j = 1
                while i+n < stop:
                    i = i+n
                    if line[i:i+n] != a:
                        break
                    j = j+1
                total = total + np.square(j)
            i = i+1    
        temp[a] = (total)
    #could change temp[a] = log(total+1),total*len(a)
    return temp


def featureMatrix(raw, prom_list):
    num_feats = [1,2,3,4,5]
    feat = list()
    comp = {}
    for i in num_feats:
        comp[i]=complist(i)

    my_list = ["TGACGTCA", "CCTCTAAAGG", "TTAATAAA", "TATA", "TTTTTCTT", "TGACTC", "TTACTAA", "TTCGGAA", "GCGGAGA", "GCGGAAA", "AAGGCAACAATAG", "CGTATCGTAT", "TTTGCTC", "AAACTGTGG", "GCGGGG", "CAGGCA", "AAGGGG", "CCGCGG", "TGCCAAG", "AAAAGAACCTCAAAAAGTCCA", "CCCCTTAAGG", "CGCG", "TTAGGG", "CATTCC", "TCTGGCACACA"]

    for a in prom_list:
        temp = list()
        line = raw[a]
        #collecting feature values
        #for a value of n
        for i in num_feats:

            features = percentACGT(line, i, comp[i])
            for item in comp[i]:
                temp.append(features[item])

            """
            features = avgACGT(line, i, comp[i])
            for item in comp[i]:
                temp.append(features[item])

            features = rightWeightedACGT(line, i, comp[i])
            for item in comp[i]:
                temp.append(features[item])

            features = leftWeightedACGT(line, i, comp[i])
            for item in comp[i]:
                temp.append(features[item])
            """
            features = lenACGT(line, i, comp[i])
            for item in comp[i]:
                temp.append(features[item])

        features = longManualACGT(line, my_list)
        ttot = 0
        for item in my_list:
            temp.append(features[item])
            ttot = ttot + features[item]
            # collected all features
        temp.append(ttot)
        feat.append(temp)
    temp = list()
    for i in num_feats:

        for item in comp[i]:
            temp.append("freq:"+str(item))
        """
        for item in comp[i]:
            temp.append("l:"+str(item))
        
        for item in comp[i]:
            temp.append("right:"+str(item))
 
        for item in comp[i]:
            temp.append("left:"+str(item))
        """
        for item in comp[i]:
            temp.append("len:"+str(item))

    for item in my_list:
            temp.append("motif:"+str(item))
    temp.append("All motif") 
    if(len(np.transpose(feat)) != len(temp)):
        print ("Error in feature vector in def featureMatrix!")
    return feat,temp

########### GENERATING FEATURES ########################
########################################################



def main():
    
    fasta_sequences = SeqIO.parse(open(sys.argv[1]),'fasta')
    raw_data = {}
    prom_list = list()
    i = 0
    j = ""
    for line in fasta_sequences:
        name, sequence = line.id, str(line.seq)
        prom_list.append(name)
        raw_data[name] = sequence[:]


    file_activity = open(sys.argv[2],"r")
    activity = {}
    for line in file_activity:
        if line == '\n':
            continue
        temp = line.split("\t")
        activity[temp[0]] = float(temp[1][:-2])

    
    X,feat_list = featureMatrix(raw_data, prom_list)
    
    for i in np.arange(0, len(X)):
        X[i].insert(0,activity[prom_list[i]])
    feat_list.insert(0,"Activity")

    
    f = open(sys.argv[3],"w")
    f.write(','.join(feat_list))
    f.write('\n')
    for line in X:
        f.write(','.join(map(str,line)))
        f.write('\n')
    f.close()

    
    
main()
            
            
            
