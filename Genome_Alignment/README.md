<h1>Genome Alignment</h1>

Genome re-sequencing (re-constructing an individual's genome from reads) is often computationally expensive. Here we attempt to come up with an efficient model.

The data [<a href="https://cm122.herokuapp.com/h1_data_files">1</a>, <a href="https://cm122.herokuapp.com/h2_data_files">2</a>] consists of paired reads. These reads are mapped to a reference genome and the variants in the donor genome are noted. The variants include, but are not limited to, SNPs, insertions and deletions. 

<h3>Burrows Wheeler Algorithm</h3>

In **basic_aligner.py**, the donor and reference sequence are aligned and the SNP variants are identified. To align the donor reads to the reference, we use the burrows wheeler transform. To allow for certain mistmatches, we assume upto 2 mismatches in a sequence and align it accordingly. Once all the reads are aligned, positions in the donor which are mapped to more mismatches than matches are identified as SNPs. To run the code on a dataset, 

```
$ python basic_aligner.py -g reference_genome.txt -r donor_reads.txt -o test_output.txt -t practice_W_1_chr_1
```

Here the input should be formatted as <a href="https://cm122.herokuapp.com/ans_file_doc">follows</a>: 
  * **reference_genome.txt**: The file with the reference genome
  * **donor_reads.txt**: The file with the donor reads (in a paired FASTA format)
  
The output is saved as **test_output.txt**. 

<h3>Hashing and LCS Backtracking</h3>

In **basic_hasher.py**, the donor and reference sequence are aligned and the SNPs, insertions and deletions are identified. To align the donor reads to the reference, taking insertions and deletions into account, we use hash maps and a back tracking algorithm to align the reads. We hash the donor sequence by the positions. Assuming 2 errors per donor read, we find an exact match to each third of the read, following which we align it to that position in the donor using a modified LCS backtracking algorithm. We align it to the first match that has 2 or fewer errors. This gives us an time and space efficient model. To run the code on a dataset,

```
$ python basic_hasher.py -g reference_genome.txt -r donor_reads.txt -o test_output.txt -t practice_E_1_chr_1
```

Here the input should be formatted as <a href="https://cm122.herokuapp.com/ans_file_doc">follows</a>: 
  * **reference_genome.txt**: The file with the reference genome
  * **donor_reads.txt**: The file with the donor reads (in a paired FASTA format)
  
The output is saved as **test_output.txt**. 

<h3>Evaluation</h3>

The model based on the Burrow Wheelers algorithm had a SNP score of 80.00 on the test data. The model based on hashing and LCS backtracking had a SNP score of 87.47 and an insertion/deletion score of 24.53 on the test data. The scores were evaluated through <a href="https://cm122.herokuapp.com/upload">heroku</a>. 
  
