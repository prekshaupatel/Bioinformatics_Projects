from scipy.stats import spearmanr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import LassoCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import RFECV
from sklearn.metrics import r2_score
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import chi2

import matplotlib.pyplot as plt


def selF(j, X, y, flist):
    rfe = RFECV(LinearRegression(), step =1, cv=5)
    X = rfe.fit(X,y.ravel())
    #selectB =SelectKBest(f_regression, k=j)
    #X = selectB.fit_transform((X), y.ravel())
    p = rfe.get_support()
    my_feat = list()

    for i in np.arange(0,len(p)):
        if p[i] == True:
            my_feat.append(flist[i])
    print ("Number of features after feature selection is", len(my_feat))
    return my_feat

            
def mod(j, X_train, y_train, train, test, flist):
    print (j)

    final = selF(j, X_train,y_train, flist)

    my_feat  = final
    #print (my_feat)
    X_train = train[my_feat]
    X_test = test[my_feat]
    y_test = test['Activity'].values.reshape(-1,1)

    """
    regr = ElasticNetCV(cv=5, random_state=0)
    regr.fit(X_train, y_train.ravel())
    print(regr.coef_)
    print ("alpha",regr.alpha_)
    rF =ElasticNet(alpha=regr.alpha_, l1_ratio = regr.l1_ratio_)
    """

    rF = LinearRegression()
    rF.fit(X_train,y_train)
    j = 0
    for i in rF.coef_:
        for k in i:
            if k != 0.0:
                j = j+1
    print ("Number of features after is ", j)


    y_pred = (rF.predict(X_train))
    print ("Train Error: ", r2_score(y_train,y_pred))
    print("correlation is ", spearmanr(np.reshape(y_train,(1,-1)),np.reshape(y_pred,(1,-1)), axis=1))
    y_new = (rF.predict(X_test))
    print("Test Error:", r2_score(y_test,y_new))
    print ("###", min(y_new), max(y_new))
    print ("##test#", min(y_test), max(y_test))
    print("correlation is ", spearmanr(np.reshape(y_test,(1,-1)),np.reshape(y_new,(1,-1)), axis = 1))

    
    return r2_score(y_train, y_pred), r2_score(y_test,y_new)



def main():
    DATAPATH = "../data/train.csv"
    train = pd.read_csv(DATAPATH)
    colnames=list()
    for col in train:
        colnames.append(col)
    X_train  = (train.drop(['Activity'], axis = 1))
    y_train = train['Activity'].values.reshape(-1,1)

    DATAPATH = "../data/test.csv"
    test = pd.read_csv(DATAPATH)
    X_test  = (test.drop(['Activity'], axis = 1))
    y_test = test['Activity'].values.reshape(-1,1)


    

    selector = VarianceThreshold()
    X_train = selector.fit_transform(X_train)

    p = selector.get_support()
    feat = list()
    for i in np.arange(0,len(p)):
        if p[i] == True:
            feat.append(colnames[i+1])


    train_score = list()
    test_score = list()
    cnt = np.arange(1,2, step=1)

    for i in cnt:
            a, b = mod(i, X_train, y_train, train, test, feat)
            train_score.append(a)
            test_score.append(b)
    """
    plt.plot(cnt, train_score, label="Training score")
    plt.plot(cnt, test_score, label = "Testing score")
    k = test_score.index(max(test_score))
    print (cnt[k]," Train: ", train_score[k]," Test: ", test_score[k])
    plt.xlabel("Number of features selected")
    plt.ylabel("r2_score")
    plt.legend()
    plt.title("Recursive Feature Elimination on scaled data")
    plt.show()
    """

main()
