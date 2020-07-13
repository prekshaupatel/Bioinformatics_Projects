<h1>Projects</h1>


<h2>Pneumonia_Detector</h2>

July, 2020

Chest x-rays are often used to identify Pneumonia patients. A machine learning model can be train to make these identifications. Here a **Neural Network** is designed and tuned to analyze the data (chest x-rays of normal individuals and pneumonia patients) and make predictions.

<code>Machine Learning</code> <code>Neural Networks</code> <code>TensorFlow</code> <code>Keras</code>


<h2>Genome_Alignment</h2>

May, 2020

Genome re-sequencing (re-constructing an individual's genome from reads using a reference genome) is often computationally expensive. Here an attempt is made to come up with an efficient model. SNP variants are identified using a **Burrows Wheeler Algorithm**. SNP variants and INDELs (Insertions/Deletions) are identified using **Hashing** and **LCS Backtracking**. 

<code>Burrows Wheeler Algorithm</code> <code>Hash Tables</code> <code>LCS Backtracking</code> 


<h2>Genome_Assembly</h2>

April, 2020

Sequencing the whole genome in one read is often too time consuming. Instead genomes are sequenced as shorter reads which are later assembled together to create the entire genome. Here we attempt to assemble the reads together, to form larger contigs - the longest donor sequence we can confidently reassemble. A **De Bruijn Graph** is constructed with the sequences and pruned. Contigs are extracted from the graph.

<code>De Bruijn Graph</code> <code>Python</code> 


<h2>Promoter_Activity_Predictor</h2>

March, 2020

The expression of genes is largely regulated by the DNA sequence upstream of it, known as the promoter region. Understanding the influence of the promoter region on gene activity is fundamental to our comprehension of natural variations in gene expression. A **Linear Regression** model, using regularization, was build to predict the promoter activity. 

<code>Machine Learning</code> <code>scikit-learn</code> <code>Linear Regression</code> <code>Ridge</code> <code>Lasso</code> <code>Elastic Net</code> 


<h2>Haplotype_Phasing</h2>

March, 2020

Genotypes are often denoted as strings of **0**s, **1**s, and **2**s, which indicates the number of copies of a reference allele at each position in the genome. Genotype also include sequencing error, which is denoted as **\*** here. To resolve the haplotypes, given the masked genotype, an **Expectation Maximization Algorithm** (EM) is implemented. The accuracy of the algorithm is evaluated using **Switch Accuracy**.

<code>Expectation-Maximization Algorithm</code> <code>Python</code>   

