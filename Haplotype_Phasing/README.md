<h1>Haplotype Phasing</h1>

The genotype for a person is given as a string containing the values {0,1,2}, indicating the number of copies of the reference allele at each SNP. In this assignment, your task is the following: conditioned on the genotypes in the file test data masked.txt, determine the haplotype phase for each person. For a genotype of 0, the phase will be (0, 0) and for a genotype of 2, the phase will be (1, 1), so the only question is how to phase the heterozygous SNPs (e.g. when the genotype is 1). These individuals are from an admixed population, but we do not know the number of ancestral populations or the number of states for each ancestral population. You can use any external data resources to infer these ancestral populations. You are not required to infer these populations, but you may do so if it helps you.

Sequencing technology is imperfect, and will produce missing (or “masked”) values for some positions of the genome. These missing values are denoted by the symbol * (as in lectures). In this project, only homozygous genotypes are missing, so * represents either 0 or 2. So, these masked values must either be imputed (e.g. guessed based on surrounding data), or taken into account by the likelihood function of your method (if you use a model with a likelihood function).

You can apply any method to the file test data masked.txt to determine the haplotype phase for these individuals. You are allowed to use methods taught in this class and/or your own ideas. Examples include Clark’s Algorithm, EM-based methods, HMM-based methods, or others. You can code in Python, R, Java, or C/C++. You are allowed to use any published methods or your own approaches to impute the missing * values. Cite all external resources in your report if you use any. You are not allowed to use published methods specifically designed for determining haplotypes from genotypes.



To phase the genotypes, run the following line of code on your shell

>>python code.py data.txt sol.txt

code.py: the given code
data.txt: replace this with the name of the file containing your genotype data
sol.txt: replace this with the name of the file to which you want to output your results to. After you run the line of code, this file will contain the phased haplotypes.
