# author: UBC Master of Data Science - Group 33
# date: 2020-11-26


"""Pre-processing wine quality data for red wine(https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv) and
   wine quality data for white wine(https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv).
   Furthermore, data is splitted into test and train data set if argument is 'n'. Ohterwise whole data is stored in 'out_dir'.

Usage: src/pre_processing_wine.py --in_file_1=<in_file_1> --in_file_2=<in_file_2> --out_dir=<out_dir> [--split=<split>]

Options:
--in_file_1=<in_file_1>      Path (including file name) to first raw data which is for red wine
--in_file_2=<in_file_2>      Path (including file name) to second raw data which is for white wine
--out_dir=<out_dir>          Path (excluding file name) of where to locally write the file
[--split=<split>]            Condsider wheater splict data or not. if --splict ='n', code will split data
"""
  
from docopt import docopt
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

opt = docopt(__doc__)

def main(in_file_1, in_file_2, out_dir, split):
  
  # read data and combine two data set vertically
  red_wine = pd.read_csv(in_file_1, sep = ";")
  white_wine = pd.read_csv(in_file_2, sep = ";")

  white_wine['type'] = 'white'
  red_wine['type'] = 'red'
  data = pd.concat([white_wine, red_wine], axis = 0)

  # add ranks for wine quality 
  conditions = [
    (data['quality'].eq(3) | data['quality'].eq(4)),
    (data['quality'].eq(5) | data['quality'].eq(6)),
    (data['quality'].eq(7) | data['quality'].eq(8) | data['quality'].eq(9))
    ]

  ranks = ['poor','normal','excellent']
  data['quality_rank'] = np.select(conditions, ranks)

  if split == "n":
    # split data as test and train
    data_train, data_test = train_test_split(data, test_size=0.2, random_state=123)
    # Save data 
    try:
      data_train.to_csv(out_dir + "processed_train.csv", index = False)
      data_test.to_csv(out_dir + "processed_test.csv", index = False)
    except:
      os.makedirs(os.path.dirname(out_dir))
      data_train.to_csv(out_dir + "processed_train.csv", index = False)
      data_test.to_csv(out_dir + "processed_test.csv", index = False)
  else:
    # Save data
    try:
      data.to_csv(out_dir + "processed.csv", index = False)
    except:
      os.makedirs(os.path.dirname(out_dir))
      data.to_csv(out_dir + "processed.csv", index = False)

if __name__ == "__main__":
  main(opt["--in_file_1"], opt["--in_file_2"], opt["--out_dir"], opt["--split"])
