import sys
import argparse
import numpy as np
import time
import zipfile

def LCSBackTrack (v, w):
    s = list()
    backtrack = list()

    for j in range(len(v)+1):
        s.append([0 for i in range(len(w)+1)])
        backtrack.append([0 for i in range(len(w)+1)])

    for i in np.arange(1,len(v)+1):
        for j in np.arange(1,len(w)+1):
            match = 1
            if v[i-1] != w[j-1]:
                match = -1

            s[i][j] = max(s[i-1][j] - 4, s[i][j-1] - 4, s[i-1][j-1] + match)
            if s[i][j] == s[i-1][j] - 4:
                backtrack[i][j] = "v";
            elif s[i][j] == s[i][j-1] - 4:
                backtrack[i][j] = "h";
            elif s[i][j] == s[i-1][j-1] + match:
                backtrack[i][j] = "d";
    end_x = 0
    end_y = len(s[0])-1
    max_val = 0
    for i in range(len(s)):
        temp = s[i][-1]
        if i > max_val:
            max_val = temp
            end_x = i

    return backtrack, max_val, [end_x , end_y], s

def UpdateDict(backtrack, v, w, i, j, s, my_dict, begin):
    temp = i + begin - 1
    if j == 0:
        return my_dict
    if i == 0:
        if temp in my_dict:
            if "dele" in my_dict[temp]: 
                my_dict[temp]["dele"].append(w[:j])
            else:
                my_dict[temp]["dele"] = [w[:j]]
        else:
            my_dict[temp] = {}
            my_dict[temp]["dele"] = [w[:j]]
        return my_dict
    if backtrack[i][j] == "v":
        if temp in my_dict:
            if "dele" in my_dict[temp]:
                my_dict[temp]["dele"].append(v[i-1])
            else:
                my_dict[temp]["dele"] = [v[i-1]]
        else:
            my_dict[temp] = {}
            my_dict[temp]["dele"] = [v[i-1]]
        return UpdateDict(backtrack, v, w, i-1, j, s, my_dict, begin)
    elif  backtrack[i][j] == "h":
        temp = temp+1
        if temp in my_dict:
            if "ins" in my_dict[temp]:
                my_dict[temp]["ins"].append(w[j-1])
            else:
                my_dict[temp]["ins"] = [w[j-1]]
        else:
            my_dict[temp] = {}
            my_dict[temp]["ins"] = [w[j-1]]
        return UpdateDict(backtrack, v, w, i, j-1, s, my_dict, begin)
    else:
        if temp in my_dict:
            if "snp" in my_dict[temp]:
                my_dict[temp]["snp"].append(w[j-1])
            else:
                my_dict[temp]["snp"] = [w[j-1]]
        else:
            my_dict[temp] = {}
            my_dict[temp]["snp"] = [w[j-1]]
        return UpdateDict(backtrack, v,w, i-1, j-1, s, my_dict, begin)


def parse_reads_file(reads_fn):
    """
    :param reads_fn: the file containing all of the reads
    :return: outputs a list of all paired-end reads
    HINT: This might not work well if the number of reads is too large to handle in memory
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
    parser = argparse.ArgumentParser(description='basic_hasher.py takes in data for homework assignment 2 consisting '
                                     'of a genome and a set of reads and aligns the reads to the reference genome, '
                                     'then calls SNPS and indels based on this alignment.')
    parser.add_argument('-g', '--referenceGenome', required=True, dest='reference_file',
                        help='File containing a reference genome.')
    parser.add_argument('-r', '--reads', required=True, dest='reads_file',
                        help='File containg sequencing reads.')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file',
                        help='Output file name.')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be outputted on the first line of the output file so that the\n'
                             'online submission system recognizes which leaderboard this file should be submitted to.\n'
                             'This HAS to be one of the following:\n'
                             '1) practice_W_3_chr_1 for 10K length genome practice data\n'
                             '2) practice_E_1_chr_1 for 1 million length genome practice data\n'
                             '3) hw2undergrad_E_2_chr_1 for project 2 undergrad for-credit data\n'
                             '4) hw2grad_M_1_chr_1 for project 2 grad for-credit data\n')
    args = parser.parse_args()
    reference_fn = args.reference_file
    reads_fn = args.reads_file

    input_reads = parse_reads_file(reads_fn)
    if input_reads is None:
        sys.exit(1)
    reference = parse_ref_file(reference_fn)
    if reference is None:
        sys.exit(1)

    length_ref = len(reference)
    hash_ref = {}
    for i in range(length_ref-15):
        seq = reference[i:i+16]
        if seq in hash_ref:
            hash_ref[seq].append(i)
        else:
            hash_ref[seq] = [i]

    threshold = 43
    pos_dict = {}
    q = 0
    for i in input_reads:
        q = q+1
        if q % 300 == 0:
            print (q,"Done")
        for j in i:
            found = False
            if j[:16] in hash_ref:
                for begin in hash_ref[j[:16]]:
                    if begin + 50 <= length_ref:
                        backtrack, val, end, s = LCSBackTrack(reference[begin:begin+50], j)
                        if val > threshold:
                            pos_dict = UpdateDict(backtrack, reference[begin:begin+50], j,
                                                  end[0], end[1], s, pos_dict, begin)
                            found = True
                            break
            if found:
                break
            if j[16:32] in hash_ref:
                for mid in hash_ref[j[16:32]]:
                    if mid - 16 >= 0 and mid + 36 <= length_ref:
                        backtrack, val, end, s = LCSBackTrack(reference[mid-16:mid+36], j)
                        if val > threshold:
                            pos_dict = UpdateDict(backtrack, reference[mid-16:mid+36], j,
                                                  end[0], end[1], s, pos_dict, mid-16)
                            found = True
                            break
            if found:
                break
            if j[-16:] in hash_ref:
                for eend in hash_ref[j[-16:]]:
                    if eend - 36 >= 0:
                        backtrack, val, end, s = LCSBackTrack(reference[eend-36:eend+16], j)
                        if val > threshold:
                            pos_dict = UpdateDict(backtrack, reference[eend-36:eend+16], j,
                                                  end[0], end[1], s, pos_dict, eend-36)
                            found = True
                            break

    snp_list = list()
    del_list = list()
    ins_list = list()
    for i in sorted(pos_dict):
        if "snp" in pos_dict[i]:
            if pos_dict[i]["snp"].count(max(pos_dict[i]["snp"])) > max(4, 0.8*len(pos_dict[i]["snp"])) and reference[i] != max(pos_dict[i]["snp"]):
                snp_list.append([reference[i], max(pos_dict[i]["snp"]), i])
        if "dele" in pos_dict[i] and len(pos_dict[i]["dele"]) > 4:
            del_list.append([reference[i],i])
        if "ins" in pos_dict[i] and len(pos_dict[i]["ins"]) > 4:
            ins_list.append([max(pos_dict[i]["ins"]), i])

    
                            
            

                        
                        
    """
        TODO: Call functions to do the actual read alignment here
    """
    
    snps = snp_list
    insertions = ins_list
    deletions = del_list

    output_fn = args.output_file
    zip_fn = output_fn + '.zip'
    with open(output_fn, 'w') as output_file:
        output_file.write('>' + args.output_header + '\n>SNP\n')
        for x in snps:
            output_file.write(','.join([str(u) for u in x]) + '\n')
        output_file.write('>INS\n')
        for x in insertions:
            output_file.write(','.join([str(u) for u in x]) + '\n')
        output_file.write('>DEL\n')
        for x in deletions:
            output_file.write(','.join([str(u) for u in x]) + '\n')
    with zipfile.ZipFile(zip_fn, 'w') as myzip:
        myzip.write(output_fn)
