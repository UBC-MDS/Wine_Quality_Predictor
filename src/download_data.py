# author: UBC Master of Data Science - Group 33
# date: 2020-11-21

"""Downloads data csv data which its delimiter is ';' from the web to a local filepath as either a csv file format.

Usage: src/down_data.py --url=<url> --out_file=<out_file>

Options:
--url=<url>              URL from where to download the data (must be in standard csv format which its delimiter is ';')
--out_file=<out_file>    Path (including filename) of where to locally write the file
"""
  
from docopt import docopt
import os
import pandas as pd

opt = docopt(__doc__)

def main(url, out_file):
  data = pd.read_csv(url,  delimiter=';')
   
  try:
    data.to_csv(out_file, index = False)
  except:
    os.makedirs(os.path.dirname(out_file))
    data.to_csv(out_file, index = False)


if __name__ == "__main__":
  main( opt["--url"], opt["--out_file"])
