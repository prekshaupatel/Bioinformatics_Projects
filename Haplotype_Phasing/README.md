<h1>Haplotype Phasing</h1>

The genotype for a person is given as a string containing the values {0,1,2}, indicating the number of copies of the reference allele at each SNP. We attempt to phase the haplotype for an individual from their genotype. 

| Genotype  | Haplotype |
| ------ | ------ |
| 0  | {0,0}  |
| 1 | {1,0}, {0,1} |
| 2 | {1,1} |
| * | {0,0}, {1,1} |

Since the haplotypes corresponding to the genotypes 0 and 2 are fixed, they are immediately resolved. An ambiguity that has to be resolved is the haplotype phase of genotype 1. Additionally, the imperfections of the sequencing technology also results in missing (masked) values, represented by **\***. In the given data, the missing values are only homozygous.   

<h3>Expectation Maximisation Algorithm</h3>

We attempt to resolve this using an EM algorithm, in python. To increase the efficiency of computation, the genotype was slit into blocks of 12 SNPs. For each genotype in the block all the possible haplotypes were computed. The haplotypes were resolved within the block by iteratively updating the probabilities associated with each possibility in the block. To improve time eficiency, the EM algorithm was run for 30 iterations, instead of till convergence. 

<h3>Running the Code</h3>

To use the data provided in the given data files, download **data.zip** and unzip it.

```
$ unzip data.zip 
```

To phase the genotypes, run the following line of code on your shell

```
$python code.py genotype.txt haplotype.txt
```

Here the files are as follows:
* **phasing.py**: the given code
* **genotype.txt**: replace this with the name of the file containing your genotype data
* **haplotype.txt**: replace this with the name of the file to which you want to output your results to. After you run the line of code, this file will contain the phased haplotypes.

<h3>Switch Accuracy</h3>

To evaluate the accuracy of the code, we compute **switch accuracy**.  

```
$ Rscript calculate_switch_accuracy.R predicted_haplotype_file true_haplotype_file
```

The accuracy and time efficiency are as follows:

| File  | Switch Accuracy | Time (Approx.) |
| ------ | ------ | ------- |
| example_data_1_masked.txt | 0.84 | ~1 hr |
| example_data_2_masked.txt | 0.86 | ~2 hr |
| test_data_masked.txt | 0.86 | ~1 hr |



