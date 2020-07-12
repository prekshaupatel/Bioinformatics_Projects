from os.path import join
import sys
import time
from collections import defaultdict, Counter
import sys
import os
import zipfile
import argparse
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))


def parse_reads_file(reads_fn):
    """
    :param reads_fn: the file containing all of the reads
    :return: outputs a list of all paired-end reads
    """
    try:
        with open(reads_fn, 'r') as rFile:
            print("Parsing Reads")
            first_line = True
            count = 0
            all_reads = []
            for line in rFile:
                count += 1
                if count % 1000 == 0:
                    print(count, " reads done")
                if first_line:
                    first_line = False
                    continue
                ends = line.strip().split(',')
                all_reads.append(ends)
        return all_reads
    except IOError:
        print("Could not read file: ", reads_fn)
        return None


"""
    TODO: Use this space to implement any additional functions you might need

"""

def contigs_gen(lines):

    graph = {}
    nodes = set()
    match = {}
    for a in lines:
        nodes.add(a[1:])
        nodes.add(a[:-1])
        if a[:-1] in match:
            match[a[:-1]].append(a[1:])
        else:
            match[a[:-1]] = [a[1:]]

    
    
    print ("0.5/10 done")
    for a in nodes:
        ls = list()
        if a in match:
            ls = match[a]
        else:
            continue

        num = len(ls)
        if  num > 1:
            temp = list()
            for i in list(set(ls)):
                if ls.count(i)*1.5 > num:
                    temp = [i]
                    break
                elif ls.count(i)*3 > num:
                    temp.append(i)
            if len(temp) > 0:
                graph[a] = temp
        
        
    print ("1/10 done")

    pre = {}
    for i in graph:
        for j in graph[i]:
            if j in pre:
                pre[j] = pre[j] + 1
            else:
                pre[j] = 1
        
    one_v_one = list()
    left = list()
    print ("2/10 done")
    for a in nodes:
        
        if a not in pre or (a in graph and len(graph[a]) > 1):
            left.append(a)
        else:
            one_v_one.append(a)


    print ("3/10 done")

    paths = list()
    pending = list()
    for a in left:
        if a in graph and len(graph[a]) > 1:
            for out in graph[a]:
                path = a+out[-1]
                while out in one_v_one and out in graph:
                    one_v_one.remove(out)
                    out = graph[out][0]
                    path = path+out[-1]
                if out in one_v_one:
                    one_v_one.remove(out)
                paths.append(path)
            
        elif a in graph:
            pending.append(a)
    print ("4/10 done")

    for a in pending:
        out = graph[a][0]
        path = a+out[-1]
        while out in one_v_one and out in graph:
            one_v_one.remove(out)
            out = graph[out][0]
            path = path+out[-1]
        if out in one_v_one:
            one_v_one.remove(out)
        paths.append(path)
    print ("5/10 done")

    for a in one_v_one:
        one_v_one.remove(a)
        out = graph[a][0]
        path = a+out[-1]
        while out in one_v_one and out in graph:
            one_v_one.remove(out)
            out = graph[out][0]
            path = path+out[-1]
        if out in one_v_one:
            one_v_one.remove(out)

        paths.append(path)


    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='basic_assembly.py takes in data for homework assignment 3 consisting '
                                                 'of a set of reads and aligns the reads to the reference genome.')
    parser.add_argument('-r', '--reads', required=True, dest='reads_file',
                        help='File containg sequencing reads.')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file',
                        help='Output file name.')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be outputted on the first line of the output file so that the\n'
                             'online submission system recognizes which leaderboard this file should be submitted to.\n'
                             'This HAS to be one of the following:\n'
                             '1) spectrum_A_1_chr_1 for 10K spectrum reads practice data\n'
                             '2) practice_A_2_chr_1 for 10k normal reads practice data\n'
                             '3) hw3all_A_3_chr_1 for project 3 for-credit data\n')
    args = parser.parse_args()
    reads_fn = args.reads_file

    input_reads = parse_reads_file(reads_fn)
    if input_reads is None:
        sys.exit(1)

    
    #        TODO: Call functions to do the actual assembly here
    my_seq = list()
    for i in range(len(input_reads)):
        my_seq = my_seq + input_reads[i]
    temp = list()
    for i in my_seq:
        for k in range(26):
            temp.append(i[k:k+25])
    
    contigs = contigs_gen(temp)

    output_fn = args.output_file
    zip_fn = output_fn + '.zip'
    with open(output_fn, 'w') as output_file:
        output_file.write('>' + args.output_header + '\n')
        output_file.write('>ASSEMBLY\n')
        output_file.write('\n'.join(contigs))
    with zipfile.ZipFile(zip_fn, 'w') as myzip:
        myzip.write(output_fn)


