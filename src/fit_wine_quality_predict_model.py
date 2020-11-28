# author: UBC Master of Data Science - Group 33
# date: 2020-11-27


""" Model building and fitting the data.
Usage: src/results/fit_wine_quality_predict_model.py --in_file_1=<in_file_1> --in_file_2=<in_file_2> --out_dir=<out_dir>
Options:
--in_file_1=<in_file_1>      Path (including file name) for the processed train data
--out_dir=<out_dir>          Path (excluding file name) of where to locally write the model
"""
from docopt import docopt
from sklearn.externals import joblib
import os
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
from sklearn.metrics import accuracy_score, log_loss, make_scorer, mean_squared_error
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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import plot_precision_recall_curve, plot_roc_curve

opt = docopt(__doc__)

def store_cross_val_results(model_name, scores, results_dict):
    """
    Stores mean scores from cross_validate in results_dict for
    the given model model_name.

    Parameters
    ----------
    model_name :
        scikit-learn classification model
    scores : dict
        object return by `cross_validate`
    results_dict: dict
        dictionary to store results

    Returns
    ----------
        None

    """
    results_dict[model_name] = {
        "mean_fit_time": "{:0.4f}".format(np.mean(scores["fit_time"])),
        "mean_score_time": "{:0.4f}".format(np.mean(scores["score_time"])),
        "mean_test_f1 (s)": "{:0.4f}".format(np.mean(scores["test_f1_micro"])),
        "mean_train_f1 (s)": "{:0.4f}".format(np.mean(scores["train_f1_micro"])),
        "mean_test_accuracy (s)": "{:0.4f}".format(np.mean(scores["test_accuracy"])),
        "mean_train_accuracy (s)": "{:0.4f}".format(np.mean(scores["train_accuracy"])),
    }

def main(in_file_1, out_dir):
    train_df = pd.read_csv(in_file_1)
    X_train = train_df.drop(columns = ['quality'], axis=1)
    y_train = train_df['quality']

    #-----------------------------------------------------------------------------------------------------------------------------
    #PreProcessor 
    numeric_features = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 
                   'chlorides', 'free sulfur dioxide','total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']
    binary_features = ['type']

    numeric_transformer = make_pipeline(SimpleImputer(), StandardScaler())
    binary_transformer = make_pipeline(OneHotEncoder(drop="if_binary", dtype=int))

    preprocessor = ColumnTransformer(
        transformers = [
            ('num', numeric_transformer, numeric_features),
            ('bin', binary_transformer, binary_features)
        ]
    )

    #-----------------------------------------------------------------------------------------------------------------------------
    #Model picking
    results_df={}
    scoring ={'accuracy', 'f1_micro'}

    pipe_iter = make_pipeline(preprocessor, MLPClassifier(random_state=1, max_iter=300))
    scores_iter = cross_validate(pipe_iter, X_train, y_train, 
                    return_train_score=True,scoring = scoring)
    store_cross_val_results(f"preprocessing + MLP", scores_iter, results_df)

    #-----------------------------------------------------------------------------------------------------------------------------
    #Hyperparameters Tuning
    rf_pipeline = make_pipeline(
    preprocessor, MLPClassifier())

    param_dist = {
        'mlpclassifier__hidden_layer_sizes': [(50,50,50), (50,100,50), (100,)],
        'mlpclassifier__activation': ['tanh', 'relu'],
        'mlpclassifier__solver': ['sgd', 'adam'],
        'mlpclassifier__alpha': [0.0001, 0.05],
        'mlpclassifier__learning_rate': ['constant','adaptive'],
        'mlpclassifier__max_iter': [300,500,450,200,300]
    }

    random_search = RandomizedSearchCV(rf_pipeline, param_distributions=param_dist, n_jobs=-1, n_iter=50, cv=5, scoring = 'f1_micro')
    random_search.fit(X_train, y_train)
    best_model_pipe = random_search.best_estimator_

    joblib_file = out_dir + "best_Model.pkl"  
    joblib.dump(best_model_pipe, joblib_file)



if __name__ == "__main__":
  main(opt["--in_file_1"], opt["--out_dir"])
