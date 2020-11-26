# Set up
import getopt
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt
from altair_saver import save


alt.renderers.enable('mimetype');
alt.data_transformers.disable_max_rows();


# ## Summary of the data set
# The data set used in this project is the results of a chemical analysis of the Portuguese "Vinho Verde" wine, conducted by [Paulo Cortez, University of Minho, Guimarães,
# Portugal](http://www3.dsi.uminho.pt/pcortez) A. Cerdeira, F. Almeida, T.
# Matos and J. Reis, Viticulture Commission of the Vinho Verde Region(CVRVV), Porto, Portugal @2009. It was sourced from the [UCI Machine
# Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality).
# 
# There are two datasets for red and white wine samples. For each wine sample observation , the inputs contains measurements of various objective physicochemical tests, and the output is the median wine quality ratings given by experts on the scale from 0 (very bad) and 10 (very excellent).The author notes that data on grape types, wine brand, wind selling price among other are not available due to privacy and logistics issues. There are 1599 observations for red wine and 4898 observations of white wine.

# ## Data Import TO BE REPLACED

def read_input_data():
    red_wine = pd.read_csv('../data/raw/winequality-red.csv', sep = ";")
    white_wine = pd.read_csv('../data/raw/winequality-white.csv', sep = ";")


    white_wine['type'] = 'white'
    red_wine['type'] = 'red'
    data = pd.concat([white_wine, red_wine], axis = 0)

    #Target distritbution plot

    distribution_plots = alt.Chart(data, title = "Distribution of wine quality").mark_bar().encode(
        alt.X('quality:Q', bin = alt.Bin(maxbins = 50), title = 'Wine quality',
            axis=alt.Axis(values=np.arange(3,10))),
        alt.Y('count():Q'),
        alt.Tooltip('count():Q')
    ).properties(height = 100)
    save(distribution_plots, 'wine_EDA_files/distribution_of_wine_quality.png')


    conditions = [
        (data['quality'].eq(3) | data['quality'].eq(4)),
        (data['quality'].eq(5) | data['quality'].eq(6)),
        (data['quality'].eq(7) | data['quality'].eq(8) | data['quality'].eq(9))
    ]

    ranks = ['poor','normal','excellent']
    data['quality_rank'] = np.select(conditions, ranks) 
# Attribution: https://stackoverflow.com/questions/54653356/case-when-function-from-r-to-python
    return data 


def generate_eda_plots(data):
    plots_dict = {}
    distribution_plots_regrouped = alt.Chart(data, title = "Distribution of wine quality (regrouped)").mark_bar().encode(
        alt.X('quality_rank:O', title = 'Wine quality rank', sort = ['poor','normal','excellent']),
        alt.Y('count():Q'),
        alt.Tooltip('count():Q')
    ).properties(width = 300, height = 300)

    distribution_of_type_of_wine = alt.Chart(data, title = "Distribution of type of wine").mark_bar().encode(
        alt.Y('type'),
        alt.X('count()'),
        alt.Color('type', legend = None),
        alt.Tooltip('count()')
    )
    plots_dict['distribution_of_type_of_wine.png'] = distribution_of_type_of_wine

    numeric_cols = data.select_dtypes('number').columns.tolist()[:-1]

    distribution_of_numeric_features = alt.Chart(data, title = "Distribution of Numeric Features").mark_bar().encode(
        alt.X(alt.repeat('repeat'), type = 'quantitative',
            bin = alt.Bin(maxbins = 50)),
        alt.Y('count()'),
    ).properties(width = 200, height = 100
    ).repeat(repeat = numeric_cols, columns = 3)

    plots_dict['distribution_of_numeric_features.png'] = distribution_of_numeric_features

    corr_df = data.select_dtypes('number').corr("spearman").stack().reset_index(name='corr')

    correlation_matrix = alt.Chart(corr_df).mark_rect(opacity=0.8).encode(
        x=alt.X('level_0', title=''),
        y=alt.Y('level_1', title=''),
        size='corr',
        color='corr')
    plots_dict['correlation_matrix.png'] = correlation_matrix


    density_rels = ['chlorides', 'residual sugar', 'volatile acidity', 'fixed acidity', 'alcohol']

    density_facet = alt.Chart(data).mark_point(size =2, opacity = 0.2).encode(
        alt.X(alt.repeat('row'), type='quantitative', scale = alt.Scale(zero = False)),
        alt.Y(alt.repeat('column'), type='quantitative', scale = alt.Scale(zero = False)),
        alt.Color('type')
    ).properties(width = 110, height = 110
    ).repeat(column = density_rels, row = ['density']
    ).configure_axis(labels=False)
    plots_dict['density_facet.png'] = density_facet

    sugar_rels = ['total sulfur dioxide','free sulfur dioxide']
    sugar_facet = alt.Chart(data).mark_point(size =2, opacity = 0.2).encode(
        alt.X(alt.repeat('row'), type='quantitative', scale = alt.Scale(zero = False)),
        alt.Y(alt.repeat('column'), type='quantitative', scale = alt.Scale(zero = False)),
        alt.Color('type')
    ).properties(width = 250, height = 250
    ).repeat(column = sugar_rels, row = ['residual sugar'])
    plots_dict['sugar_facet.png'] = sugar_facet



    wine_quality_rank = alt.Chart(data, title="Wine Quality Rank").mark_bar().encode(
        x=alt.X('count()'),
        y='type',
        color='quality_rank'
    )
    plots_dict['wine_quality_rank.png'] = wine_quality_rank


    wine_quality_rank_per_feature = alt.Chart(data).mark_boxplot().encode(
        alt.Y('quality_rank'),
        alt.X(alt.repeat('repeat'), type = 'quantitative', scale = alt.Scale(zero = False)), 
        alt.Color('quality_rank')
    ).properties(width = 200, height = 100
    ).repeat(repeat = numeric_cols, columns = 3)
    plots_dict['wine_quality_rank_per_feature.png'] = wine_quality_rank_per_feature
    return plots_dict


def save_plots(output_dir, plots_dict):
    for k, v in plots_dict.items():
        try:
            save(v, output_dir + "/" + k)
            print("Successfully saved {}".format(k))
        except Exception as e:
            print(e)

def main(input_path, output_dir):
    data = read_input_data()
    plots_dict = generate_eda_plots(data)
    save_plots(output_dir, plots_dict)


def usage():
    print ("""
    Usage: python %s [-h|-i|-o] [--help|--input|--output]
    If you couldn't export the png files, please make sure you properly installed node js packaged below:
    npm install -g --force vega-lite vega-cli canvas
    conda install -c conda-forge vega-cli vega-lite-cli 
    Options:
        -h, --help          Print help message
        -i, --input         Input data file path
        -o, --output        Output data file path
    """ % sys.argv[0])


if __name__ == '__main__':
    input_path = None
    output_path = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", [
            "help", "--input", "--output"
        ])
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                exit()
            if o in ('-i', '--input'):
                input_path = a
            if o in ('-o', '--output'):
                output_path = a
        main(input_path, output_path)
    except Exception as e:
        print(e)
