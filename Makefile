# Wine Quality Predictor (makefile)
# author: Group 33
# date: 2020-12-04

# This driver script completes the analysis on wine quality and generate 
# a model for wine quality predictor and corresponding report.
# It takes no arguments.

# example usage:
# make all

all: results/best_Model.pkl reports/reports.md

# download wine data set to directory
data/raw/winequality-red.csv : src/download_data.py
	python src/download_data.py --url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv" --out_file="data/raw/winequality-red.csv"

data/raw/winequality-white.csv : src/download_data.py	
	python src/download_data.py --url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv" --out_file="data/raw/winequality-white.csv"

# pre-process data and split data to training set and test set
data/processed/processed_test.csv data/processed/processed_train.csv : src/pre_processing_wine.py data/raw/winequality-red.csv data/raw/winequality-white.csv
	python src/pre_processing_wine.py --in_file_1="data/raw/winequality-red.csv" --in_file_2="data/raw/winequality-white.csv" --out_dir="data/processed/"

# create exploratory data analysis figure and write to file
eda/wine_EDA_files/wine_quality_rank_per_feature.png : python eda/wine_eda.py data/processed/processed.csv
	python eda/wine_eda.py -i data/processed/processed.csv -o eda/wine_EDA_files/

# fitting model
results/best_Model.pkl : src/fit_wine_quality_predict_model.py data/processed/processed_train.csv
	python src/fit_wine_quality_predict_model.py --in_file_1="data/processed/processed_train.csv" --out_dir="results/"

# test model
results/final_model_quality.png : src/wine_quality_test_results.py data/processed/processed_train.csv data/processed/processed_test.csv results/best_Model.pkl
	python src/wine_quality_test_results.py --in_file_1="data/processed/processed_train.csv" --in_file_2="data/processed/processed_test.csv" --out_dir="results/"

# render final report
reports/reports.md : reports/reports.Rmd reports/wine_refs.bib
	Rscript -e "rmarkdown::render('reports/reports.Rmd', output_format = 'github_document')"

clean: 
	rm -rf data
	rm eda/wine_EDA_files/wine_quality_rank_per_feature.png
	rm -rf results
	rm reports/reports.md
	
	
			
