# author: UBC Master of Data Science - Group 33
# date: 2020-11-26


"""Pre-processing wine quality data for red wine(https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv) and
   wine quality data for white wine(https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv).

Usage: src/wine_quality_test_results_test.py --in_file_1=<in_file_1> --in_file_2=<in_file_2> --out_dir=<out_dir>

Options:
--in_file_1=<in_file_1>      Path (including file name) to the processed train data
--in_file_2=<in_file_2>      Path (including file name) to the processed test data
--out_dir=<out_dir>          Path (excluding file name) to save the confusion matrix
"""
import os
from docopt import docopt
import string
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data
from sklearn import datasets
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer

# Feature selection
from sklearn.feature_selection import RFE, RFECV
from sklearn.impute import SimpleImputer

# classifiers / models
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import LogisticRegression

# other
from sklearn.metrics import accuracy_score, log_loss, make_scorer, mean_squared_error, confusion_matrix
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    ShuffleSplit,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.neural_network import MLPClassifier
import joblib
from sklearn.metrics import (plot_confusion_matrix)



opt = docopt(__doc__)

def main(in_file_1, in_file_2, out_dir):
    # read data and splitting it
    train_df = pd.read_csv(in_file_1)
    test_df = pd.read_csv(in_file_2)

    X_train = train_df.drop(columns = ['quality','quality_rank'], axis=1)
    y_train = train_df['quality_rank']
    X_test = test_df.drop(columns = ['quality','quality_rank'], axis=1)
    y_test = test_df['quality_rank']


    #---------------------------------------------------------------------------------------------------------
    # Testing out model

    best_model_pipe = joblib.load("results/best_Model.pkl")
    best_model_pipe.fit(X_train, y_train)
    best_model_pipe.score(X_test, y_test)

    plot_confusion_matrix(best_model_pipe, X_test, y_test, cmap = plt.cm.Blues, normalize='true')
    predictions_m = best_model_pipe.predict(X_test)
    cm = confusion_matrix(y_test, predictions_m)
    path_f = out_dir + "final_model_quality.png"
    plt.savefig(path_f)
    

if __name__ == "__main__":
  main(opt["--in_file_1"], opt["--in_file_2"], opt["--out_dir"])
