<h1>Predicting Promoter Activity from Promoter Region Sequence</h1>

<h3>Abstract</h3>

The expression of genes is largely regulated by the DNA sequence upstream of it, known as the promoter region. Understanding the influence of the promoter region on gene activity is fundamental to our comprehension of natural variations in gene expression. To this extent, various models have been developed to predict the promoter activity from the promoter region DNA sequence. As a solution to the <a href="https://www.synapse.org/#!Synapse:syn2820426/wiki/">DREAM challenge</a>, <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4916984/">Siwo, et al. (2016)</a> proposed a support vector machine model to predict promoter activities in yeast. Their model predicted promoter activities with a spearman correlation of 0.73 in natural sequences and 0.57 in laboratory mutated sequences. However, there is potential to improve the accuracy of the predictions.

The proposed hypothesis is that a linear regression model could be implemented to predict the promoter activity from the promoter sequence. To build a model, features were extracted from the sequence including frequency of k-mers (k=1-5), sum of position of k-mers, number of occurrences of k-mers, and number of occurrences of known motifs <a href="https://www.sciencedirect.com/science/article/pii/S1097276508008423">(Badis, et al., 2008)</a>. Feature selection and regularization (Ridge, Lasso, and Elastic Net), using <a href="https://scikit-learn.org/stable/">scikit-learn</a> in python, were implemented to avoid overfitting. In addition, hyperparameters selected for the regularization models were optimized with a grid search using 5-fold cross-validation. Using the optimized hyperparameters, the model was trained on the training dataset. The accuracy of prediction on the test data indicated that an elastic net model without feature selection performed the best (R<sup>2</sup> regression score of 0.229). In the future, the accuracy of the model can be improved by using a larger sample size to train the model, by selecting more relevant features, and by exploring non-linear models.

<h3>Running the Code</h3>

To run the code, download the **src** and **data** directories. Navigate into the src directory. 

```
$ cd src
```

To extract certain features to train the model, modify the **feature.py** file. Run the code to extract the features and save them in the **data** directory. These features are used to train the model.

```
$ python feature.py
```

Once the features are extracted from the promoter region sequence, the model can be run on those features by running the **model.py** file. The file can be slightly modified to change the feature selection/regularization methods.


```
$ python model.py
```
