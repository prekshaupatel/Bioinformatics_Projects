<h1>Assembling the Genome</h1>

Sequencing the whole genome in one read is often too time consuming. Instead genomes are sequenced as shorter reads which are later assembled together to create the entire genome. Here we attempt to assemble the reads together, to form larger contigs - the longest donor sequence we can confidently reassemble.

The <a href="https://cm122.herokuapp.com/h3_data_files">data</a> consist of donor reads and also some random reads to mimic contamination. We assemble the reads to form a **de bruijn graph** and then traverse it to extract the longest nonbranching-paths. These are our contigs. To obtain longer and more accurate contigs, we prune the de bruijn graph before traversing it.

To run the assembler,

```
$ python3 basic_assembly.py -r reads.txt -o test_output.txt -t practice_A_2_chr_1
```

Here the input should be formatted as <a href="https://cm122.herokuapp.com/ans_file_doc">follows</a>: 
  * **reads.txt**: The file with the donor reads (in a paired FASTA format)
  
The output is saved as **test_output.txt**. 

The model obtained a **coverage score** of 87.94, a **contig sizes score** of 7.97, and a **accuracy score** of 48.00. The scores were evaluated through <a href="https://cm122.herokuapp.com/upload">heroku</a>.
