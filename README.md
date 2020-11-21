# Wine Quality Predictor

contributors: 
Member | Github
-------|---------
Bruhat Musunuru |[bruhatm](https://github.com/BruhatM)
Alex Truong Hai Yen | [athy9193](https://github.com/athy9193)
Rui Wang |[wang-rui](https://github.com/wang-rui)
Sang Yoon Lee |[rissangs](https://github.com/rissangs)

First milestone of a data analysis project for DSCI 522 (Data Science workflows, part of Master of Data Science program at the University of British Columbia.)

## Introduction

In this project we are trying to predict the quality of a given wine sample using its features, composition and characteristics. Traditional methods of categorizing wine are prone to human error and can vary drastically from expert to expert. We propose a data mining approach to predict human wine taste preferences based on complex data analytical algorithms and classification models. This unbiased and human error free metric can provide a standardized metric that can be used for personalized wine recommendation, Quality assessment and comparison unit. It can also be used by wineries as an important metric which could aid in important business decisions and strategies.
	
  The data set used in this project is created by Paulo Cortez from the University of Minho in Guimarães, Portugal, and A. Cerdeira, F. Almeida, T. Matos and J. Reis from the Viticulture Commission of the Vinho Verde Region in Porto, Portugal. The two datasets are included are related to red and white vinho verde wine samples, from the north of Portugal. It was sourced from the UCI Machine Learning Repository and can be found [here](https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/). Each row in the data set represents summary statistics from a sample of wine based on physicochemical tests with attributes fixed acidity, volatile acidity, citric acid, residual sugar, pH, etc.  

  We plan to build a predictive classification model to provide the standardized metric discussed above. In order for the model to abide by the golden rule, we plan to split the data into train and test sets (80% - 20% respectively) and perform exploratory data analysis in order to assess any class imbalance, outliers that needs to be considered when scouting for best model to fit our needs. After the EDA, we see that wine quality ranking seems to be more likely to associate with alcohol, density, free sulfur dioxide, volatile acidity, wine type than the rest of the input features. Hence a multiclass linear classification could be appropriate to estimate the impact each features have on wine quality ranking.
	
  The outcome or the Standardized metric we are trying to establish is to classify all wines into three classes (Poor, Normal, Excellent). One likely model suitable for this classification is linear regression and set a threshold for each class in the predicted probabilities. Since our data set is reasonably sized with 1598 observations, we can choose a higher cross-validation of ~50 folds. We will use this accuracy to tune our model for the best fit. After doing so, we re-fit the model on the entire training data set, and then evaluate it’s performance on the test data set. This gives a deeper understanding of our model. We will use this information to address classification errors and report them as a table in the final report.

For this Milestone we have performed an EDA on the data set which can be found <a href=https://github.com/UBC-MDS/Wine_Quality_Predictor/blob/main/eda/wine_EDA.md>here</a>
 



## Usage

To replicate the analysis, clone this GitHub repository, install the
[dependencies](#dependencies) listed below, and run the following
commands at the command line/terminal from the root directory of this
project: 

1. Create a conda envrioment using the `wine_env.yml`
```bash
conda env create --file wine_env.yml
conda activate wine_env
```
2. Download wine data set in data directory
```bash
python src/download_data.py --url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv" --out_file="data/winequality-red.csv"
python src/download_data.py --url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv" --out_file="data/winequality-white.csv"
```
## Dependencies

To run this project, please install the required dependencies from [here](https://github.com/UBC-MDS/Wine_Quality_Predictor/blob/main/wine_env.yml)

## License

The Wine Quality Predictor materials here are licensed under the
Creative Commons Attribution 2.5 Canada License (CC BY 2.5 CA). If
re-using/re-mixing please provide attribution and link to this webpage.

# References

<div id="refs" class="references">

<div>

Paulo Cortez, University of Minho, Guimarães, Portugal, http://www3.dsi.uminho.pt/pcortez
A. Cerdeira, F. Almeida, T. Matos and J. Reis, Viticulture Commission of the Vinho Verde Region(CVRVV), Porto, Portugal
@2009
</div>

<div>

P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009. https://archive.ics.uci.edu/ml/datasets/Wine+Quality

</div>

<div>
  
Sample Milestone 1 on Breast Cancer for 552 by author: Tiffany Timbers, contributors: Melissa Lee. https://github.com/ttimbers/breast_cancer_predictor/tree/v1.1

</div>

</div>

