Predicting wine quality using measurements of physiochemical tests
================
Alex Truong, Bruhat Musinuru, Rui Wang and Sang Yoon Lee </br>
2020-11-26 (updated: 2020-11-28)

  - [Summary](#summary)
  - [Introduction](#introduction)
  - [Methods](#methods)
      - [Data](#data)
      - [Analysis](#analysis)
  - [Results & Discussion](#results-discussion)
  - [References](#references)

## Summary

For this analysis, we conduct the {neutral network Multi-layer
Perception (MLP) model} in order to try to predict the different wine
quality based on the wine attributes obtained from various
physicochemical tests such as alcohol, sulfur diocide, fixed acidity,
residual sugar. The results showed that {MPL yield robust results} with
80% accuracy and 80% f1- score (i.e. a weighted average metric of the
precision and recall) on validation set. When we run the model on our
test set, we also have comparably high score at 80% accuracu and
f1-score. However, it incorrectly predicts {XX cases from normal wine to
be excellent wine - talk about confusion matrix}.

As the rate of misclassification is not high and the impact can be
corrected in further assessment, we believe this model could decent
serve its purpose as a wine predictor to conduct first-cut wine
classification, which could help speed up the wink ratings process.

## Introduction

Traditional methods of categorizing wine are prone to human error and
can vary drastically from expert to expert. We propose a data mining
approach to predict wine quality using machine learning techniques for
classification problems. The resulting model, we hope, could serve as as
one of scientific and systematic ways to classify wine, which is a
springboard for further research in personalized wine recommendation,
quality assessment and comparison unit.

Moreover, we believe wineries or wine rating institutes could find the
model as a useful and reliable first-cut wine quality test before
further expert’s assessment. This could lead to a more cost and
time-effective wine screening process, and subsequently facilitate more
effective and efficient business decisions and strategies.

## Methods

### Data

The data set used in this project is the results of a chemical analysis
of the Portuguese “Vinho Verde” wine, conducted by Paulo Cortez, A.
Cerdeira, F. Almeida, T. Matos and J. Reis (Cortez et al. 2009). It was
sourced from the UCI Machine Learning Repository (Dua and Graff 2017)
which can be found
[here](https://archive.ics.uci.edu/ml/datasets/wine+quality).

There are two datasets for red and white wine samples. For each wine
sample observation , the inputs contains measurements of various
objective physicochemical tests, and the output is the median wine
quality ratings given by experts on the scale from 0 (very bad) and 10
(very excellent).The author notes that data on grape types, wine brand,
wind selling price among other are not available due to privacy and
logistics issues. There are 1599 observations for red wine and 4898
observations of white wine.

### Analysis

At the preprocessing stage, we decided to combine the red and white data
set as well as group the data in bigger classification, namely “poor”,
“normal” and “excellent” for scale “1-4”, “5-6” and “7-9” so as to
have bigger sample size. We acknowledge that the data is imbalanced,
hence instead of only using accuracy based to judge the model
performance, we also include f1-score and use it as our main assessment
metric. f-1 score is metric that combine both the precision and recall
metrics, which focus on the false negative and false positive rate of
the data and would be appropriate to use with an imbalanced data set.

In this project we are trying to predict the quality of a given wine
sample using wine attributes obtained from various physicochemical tests
and the {neutral network Multi-layer Perception (MLP) model. We decided
to pick this model as the model that yield the best after running the
various machine learning model through the train dataset and comparing
their performance based on f1-score}

{write more about paper}

The Python and R programming languages (R Core Team 2019; Van Rossum and
Drake 2009) and the following Python and R packages were used to perform
the analysis: scikit-learn (Pedregosa et al. 2011), docoptpython
(Keleshev 2014), docopt (de Jonge 2018), knitr (Xie 2014), tidyverse
(Wickham 2017), kableExtra (Zhu 2020) {to add more based on revised
yml}. The code used to perform the analysis and re-create this report
can be found
[here](https://github.com/athy9193/Wine_Quality_Predictor#usage)

## Results & Discussion

Looking at the distribution plot of the respective wine quality group
interacting with each explanatory features, we can see that higher
quality wine seems to be more associated with higher `alcohol` level and
lower `density`. Lower `volatile acidity` also seems to be indicative of
better wine. Better ranked wine also seem to have `higher free sulfur
dioxide` level than poor wine though the relationship is not that clear
based on the plot. The rest of the features do not seems be very
distinguishable among different quality wine.

<img src="../eda/wine_EDA_files/wine_quality_rank_per_feature.png" width="939" />

{To discuss the results from multi-class ridge, paper} {To add the
result table} {PLACE HOLDER FROM MILESTONE 1, TO REVISED We plan to
build a predictive classification model to provide the standardized
metric discussed above. In order for the model to abide by the golden
rule, we plan to split the data into train and test sets (80%-20%
respectively) and perform exploratory data analysis in order to assess
any class imbalance, outliers that needs to be considered when scouting
for best model to fit our needs. After the EDA, we see that wine quality
ranking seems to be more likely to associate with alcohol, density, free
sulfur dioxide, volatile acidity, wine type than the rest of the input
features. Hence a multiclass linear classification could be appropriate
to estimate the impact each features have on wine quality ranking.

The outcome or the Standardized metric we are trying to establish is to
classify all wines into three classes (Poor, Normal, Excellent). One
likely model suitable for this classification is linear regression and
set a threshold for each class in the predicted probabilities. Since our
data set is reasonably sized with 1598 observations, we can choose a
higher cross-validation of \~50 folds. We will use this accuracy to tune
our model for the best fit. After doing so, we re-fit the model on the
entire training data set, and then evaluate it’s performance on the test
data set. This gives a deeper understanding of our model. We will use
this information to address classification errors and report them as a
table in the final report.}

Having said that the research also need further improvement in terms of
obtaining a more balanced data set for training and cross-validation.
More feature engineer and selection could be conducted to minimize the
affect of correlation among the explanatory variable. Furthermore, in
order to assess the robustness of the predicting model, we need to test
the model with deployment data in real world besides testing with our
test data.

# References

<div id="refs" class="references hanging-indent">

<div id="ref-cortez2009modeling">

Cortez, Paulo, António Cerdeira, Fernando Almeida, Telmo Matos, and José
Reis. 2009. “Modeling Wine Preferences by Data Mining from
Physicochemical Properties.” *Decision Support Systems* 47 (4): 547–53.

</div>

<div id="ref-docopt">

de Jonge, Edwin. 2018. *Docopt: Command-Line Interface Specification
Language*. <https://CRAN.R-project.org/package=docopt>.

</div>

<div id="ref-Dua:2019">

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.”
University of California, Irvine, School of Information; Computer
Sciences. <http://archive.ics.uci.edu/ml>.

</div>

<div id="ref-docoptpython">

Keleshev, Vladimir. 2014. *Docopt: Command-Line Interface Description
Language*. <https://github.com/docopt/docopt>.

</div>

<div id="ref-scikit-learn">

Pedregosa, F., G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O.
Grisel, M. Blondel, et al. 2011. “Scikit-Learn: Machine Learning in
Python.” *Journal of Machine Learning Research* 12: 2825–30.

</div>

<div id="ref-R">

R Core Team. 2019. *R: A Language and Environment for Statistical
Computing*. Vienna, Austria: R Foundation for Statistical Computing.
<https://www.R-project.org/>.

</div>

<div id="ref-Python">

Van Rossum, Guido, and Fred L. Drake. 2009. *Python 3 Reference Manual*.
Scotts Valley, CA: CreateSpace.

</div>

<div id="ref-tidyverse">

Wickham, Hadley. 2017. *Tidyverse: Easily Install and Load the
’Tidyverse’*. <https://CRAN.R-project.org/package=tidyverse>.

</div>

<div id="ref-knitr">

Xie, Yihui. 2014. “Knitr: A Comprehensive Tool for Reproducible Research
in R.” In *Implementing Reproducible Computational Research*, edited by
Victoria Stodden, Friedrich Leisch, and Roger D. Peng. Chapman;
Hall/CRC. <http://www.crcpress.com/product/isbn/9781466561595>.

</div>

<div id="ref-kableExtra">

Zhu, Hao. 2020. *KableExtra: Construct Complex Table with ’Kable’ and
Pipe Syntax*. <https://CRAN.R-project.org/package=kableExtra>.

</div>

</div>
