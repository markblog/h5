__author__ = 'V631932'

from InterestMeasureFormater import interest_point
import pandas as pd

prdatafile_path = 'D:\\AI PROJECT_NEWDATA\PR_datafiles'
prtagfile_path = 'D:\\AI PROJECT_NEWDATA\PR_tagfiles'
chart_name = 'P00081_ALL__TOP_10_BMV.csv'
datafile = pd.read_csv(prdatafile_path + '\\' + chart_name)
tagfile = pd.read_csv(prtagfile_path + '\\' + chart_name)
chart_name_short = chart_name.split('.')[0]

ip = interest_point(prdatafile_path, prtagfile_path)
a, b = ip.evalutefromdf(datafile, tagfile, chart_name_short)
print(a)
print(b)