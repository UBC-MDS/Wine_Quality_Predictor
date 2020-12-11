# author: UBC Master of Data Science - Group 33
# date: 2020-11-28


"""Selecting Multi-layer Perception(MLP) modle as best model and save plots for report.
Optimizes hyperprameter for MLP model and fits a MLP model with best hyperparameter on the pre-processed training data from UCI Machine Learning Repository.
Saves the model as a pkl file.

Usage: src/fit_wine_quality_predict_model.py --in_file_1=<in_file_1> --out_dir=<out_dir> 

Options:
--in_file_1=<in_file_1>      Path (including file name) to first raw data which is for red wine
--out_dir=<out_dir>          Path (excluding file name) of where to locally write the file

"""
  
from docopt import docopt
import joblib
import os
import string
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt

# Sklearn dependencies
from sklearn import datasets
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import (accuracy_score, 
    log_loss, make_scorer, 
    mean_squared_error, 
    plot_confusion_matrix
)
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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from altair_saver import save


opt = docopt(__doc__)

def main(in_file_1, out_dir):
    # read data and combine two data set vertically
    train_df = pd.read_csv(in_file_1)
    X_train = train_df.drop(columns = ['quality','quality_rank' ])
    y_train = train_df['quality_rank']
    
    #-----------------------------------------------------------------------------------------------------------------------------
    # PreProcessor 
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
    # Model selection
    results={}
    scoring_metric = {'f1_micro'}
    classifiers_plot = {
        "RidgeClassifier": RidgeClassifier(random_state=123),
        "Random Forest":RandomForestClassifier(bootstrap=False, max_depth=20,
                                            max_features='sqrt', n_estimators=1800,
                                            random_state=123),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "MLP Classifier":MLPClassifier(alpha=0.05, hidden_layer_sizes=(50, 100, 50),
                                learning_rate='adaptive', max_iter=1000,random_state=123),
        "Nearest Centroid": NearestCentroid(),
        "QDA" :QuadraticDiscriminantAnalysis()
    }
    
    for (name, model) in classifiers_plot.items():
        pipe_iter = make_pipeline(preprocessor, model)
        results[name] = mean_std_cross_val_scores(pipe_iter, 
                                                  X_train, 
                                                  y_train, 
                                                  return_train_score=True, 
                                                  scoring=scoring_metric)
    
    pd.DataFrame(results)
    #---------------------------------------------------------------------------------------------------------
    # Plotting result
    # All classifiers
    plots_dict={}
    plot_results = pd.DataFrame(results).T
    plot_results =plot_results.reset_index()
    bar_all = alt.Chart(plot_results).mark_bar().encode(
        alt.X('test_f1_micro', axis=alt.Axis(title='F1 Micro score')),
        alt.Y('index', sort='-x', axis=alt.Axis(title='Classifier')),
    ).properties(
        width=alt.Step(40)  # controls width of bar.
    )

    plots_dict['f1_score_all_classifiers.png'] = bar_all
    
    # Stability across cv folds
    scoring_metric = {'f1_micro'}
    pipe_rf = make_pipeline(preprocessor,
                            RandomForestClassifier(bootstrap=False, 
                                                   max_depth=20,
                                                   max_features='sqrt', 
                                                   n_estimators=1800,
                                                   random_state=123))
    scores_rf = cross_validate(pipe_rf, 
                               X_train, 
                               y_train, 
                               return_train_score=True,
                               scoring = scoring_metric, 
                               n_jobs=-1, 
                               cv=20)

    plot_rf = pd.DataFrame(scores_rf)
    bar_rf = alt.Chart(plot_rf).mark_bar().encode(
        x= alt.X('test_f1_micro', axis=alt.Axis(title='F1 Micro score'), bin=alt.Bin(extent=[0.75, 0.9], step=0.02)),
        y= alt.Y('count()'),
    )
    
    plots_dict['f1_score_random_forest.png'] = bar_rf

    pipe_mlp = make_pipeline(preprocessor, 
                             MLPClassifier(alpha=0.05, 
                                           hidden_layer_sizes=(50, 100, 50),
                                          learning_rate='adaptive', 
                                          max_iter=1000,
                                          random_state=123))
    
    scores_mlp = cross_validate(pipe_mlp,
                                X_train,
                                y_train, 
                                return_train_score=True,
                                scoring = scoring_metric,
                                n_jobs=-1,
                                cv=20 )

    plot_mlp = pd.DataFrame(scores_mlp)
    bar_mlp = alt.Chart(plot_mlp).mark_bar().encode(
        x= alt.X('test_f1_micro', axis=alt.Axis(title='F1 Micro score'), bin=alt.Bin(maxbins=6)),
        y= alt.Y('count()'),
    )

    plots_dict['f1_score_mlp.png'] = bar_mlp

    save_plots(out_dir, plots_dict)

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
    
    try:
        joblib_file = out_dir + "best_Model.pkl"  
        joblib.dump(best_model_pipe, joblib_file)
    except:
        os.makedirs(os.path.dirname(out_dir))
        joblib_file = out_dir + "best_Model.pkl"  
        joblib.dump(best_model_pipe, joblib_file)

def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean and std of cross validation
    """
    scores = cross_validate(model, 
                            X_train, y_train, n_jobs=-1, 
                            **kwargs)    
    
    mean_scores = pd.DataFrame(scores).mean()
    #std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):  
        out_col.append(mean_scores[i])

    return pd.Series(data = out_col, index = mean_scores.index)

def save_plots(output_dir, plots_dict):
    if os.path.exists(output_dir):
        pass
    else:
        os.makedirs(os.path.dirname(output_dir))
    
    for k, v in plots_dict.items():
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            save(v, output_dir + k, method='selenium', webdriver=driver)
            print("Successfully saved {}".format(k))
        except Exception as e:
            print(e)

if __name__ == "__main__":
  main(opt["--in_file_1"], opt["--out_dir"])