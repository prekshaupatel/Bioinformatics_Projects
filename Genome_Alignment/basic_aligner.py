import sys
import argparse
import time
import zipfile



def code_trans(line):                                                                    
    line = line+"$"
    ls = list()
    for i in range(len(line)):
        ls.append(line[i:]+line[:i])

    t = [i[-1] for i in sorted(ls)]

    return t


def func(first, last):
    trans = {}
    lett = "$"
    k = 1
    word = 0
    while word+1 < len(last):
        ind = 0
        for i in range(k):
            ind = ind + last[ind:].index(lett)+1
        ind = ind - 1
        lett=first[ind]
        trans[ind] = word
        word = word + 1

        k = first[:ind+1].count(lett)
    trans[0] = word
    return trans

def pos_for_seq(patt, max_misses, lastToFirst, first, last):

    best_pos = -1
    least_misses = 100
    n_miss, n_pos = find_positions(patt, max_misses, lastToFirst, first, last)
    if n_miss == 0:

        return n_pos
    least_misses = n_miss
    best_pos = n_pos

    for i in range(max_misses):
        n_miss, n_pos = find_positions(patt[:-1-i], max_misses-1-i, lastToFirst, first, last)
        if n_miss == 0:

            return n_pos
        elif n_miss < least_misses:
            least_misses = n_miss
            best_pos = n_pos

    if least_misses > max_misses:
        return -1
    return best_pos


    return list(set(poss))

def find_positions(patt, max_misses, lastToFirst, first,last):

    positions = list()
    my_pattern = list(patt)
    lett = my_pattern.pop(-1)
    print lett
    ind = range(first.index(lett), first.index(lett)+first.count(lett), 1)
    misses = [0 for i in ind]

    while len(my_pattern) > 0 and len(ind) > 0:
        lett = my_pattern.pop(-1)
        new = [0 for i in ind]
        i = 0
        while i < len(ind):
            new[i] = lastToFirst[ind[i]]
            if last[ind[i]] != lett:
                if misses[i] >= max_misses or last[ind[i]] == "$":
                    misses.pop(i)
                    new.pop(i)
                    ind.pop(i)
                    i = i-1
                else:
                    misses[i] = misses[i] + 1
            i = i+1
        ind = new

    if len(misses) == 0:
        return 100, -1
    least_misses = min(misses)
    best_pos = ind[misses.index(least_misses)]
    return least_misses, best_pos









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


def parse_ref_file(ref_fn):
    """
    :param ref_fn: the file containing the reference genome
    :return: a string containing the reference genome
    """
    try:
        with open(ref_fn, 'r') as gFile:
            print("Parsing Ref")
            first_line = True
            ref_genome = ''
            for line in gFile:
                if first_line:
                    first_line = False
                    continue
                ref_genome += line.strip()
        return ref_genome
    except IOError:
        print("Could not read file: ", ref_fn)
        return None


"""
    TODO: Use this space to implement any additional functions you might need

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='basic_aligner.py takes in data for homework assignment 1 consisting '
                                     'of a genome and a set of reads and aligns the reads to the reference genome, '
                                     'then calls SNPs based on this alignment')
    parser.add_argument('-g', '--referenceGenome', required=True, dest='reference_file',
                        help='File containing a reference genome.')
    parser.add_argument('-r', '--reads', required=True, dest='reads_file',
                        help='File containg sequencing reads.')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file',
                        help='Output file name.')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be outputted on the first line of the output file so that the '
                             'online submission system recognizes which leaderboard this file should be submitted to.'
                             'This HAS to be practice_W_1_chr_1 for the practice data and hw1_W_2_chr_1 for the '
                             'for-credit assignment!')
    args = parser.parse_args()
    reference_fn = args.reference_file
    reads_fn = args.reads_file

    input_reads = parse_reads_file(reads_fn)

    if input_reads is None:
        sys.exit(1)
    reference = parse_ref_file(reference_fn)
    if reference is None:
        sys.exit(1)

    """
        TODO: Call functions to do the actual read alignment here
        
    """
    print ("Calling my functions")

    patterns = list()
    for i in input_reads:
        patterns = patterns+i

    max_misses = 2
    line = reference

    last = code_trans(line)
    first = sorted(last)



    firstToPos = func(first, last)
    lastToFirst = {}

    for i in range(len(last)):
        k = last[:i].count(last[i])
        lastToFirst[i] = first.index(last[i]) + k

    sol = {}
    for patt in patterns:
        temp2 = pos_for_seq(patt, max_misses, lastToFirst, first, last)
        if temp2 != -1:
            sol[patt] = firstToPos[temp2]

    lett = [[] for i in range(len(line))]
    for i in sol:
        start = sol[i]
        for j in range(len(i)):
            lett[start+j].append(i[j])

    finale = list()
    for i in range(len(line)):
        if len(lett[i]) == 0:
            continue
        t = max(set(lett[i]), key = lett[i].count)
        if t != line[i]:
            finale.append([line[i], t, i])







    snps = finale

    output_fn = args.output_file
    zip_fn = output_fn + '.zip'
    with open(output_fn, 'w') as output_file:
        header = '>' + args.output_header + '\n>SNP\n'
        output_file.write(header)
        for x in snps:
            line = ','.join([str(u) for u in x]) + '\n'
            output_file.write(line)

        tails = ('>' + x for x in ('STR', 'CNV', 'ALU', 'INV', 'INS', 'DEL'))
        output_file.write('\n'.join(tails))

    with zipfile.ZipFile(zip_fn, 'w') as myzip:
        myzip.write(output_fn)
