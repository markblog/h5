import pandas as pd

from .DatafileFormated import DatafileFormated
from .ChartPortraitsWriter import chart_portraits
import glob
import os
import warnings
warnings.filterwarnings("ignore")


tagfile_path = "D:\\AI PROJECT_NEWDATA\\PR_tagfiles"
path = "D:\\AI PROJECT_NEWDATA"
allfiles = glob.glob(os.path.join(tagfile_path,"**", "*.csv"), recursive=True)
allfilenames = [x.split('\\')[-1] for x in allfiles]
cp = chart_portraits()
for i, file_name in enumerate(allfilenames):

    narrative_point = list(pd.read_csv(allfiles[i])['Narrative_element'])[0]
    print(file_name, narrative_point)
    datafile = pd.read_csv(path + "\\PR_datafiles\\" + file_name)
    tagfile = pd.read_csv(path + "\\PR_tagfiles\\" + file_name)
    chart_name = file_name.split(".")[0]


    datafileFormated = DatafileFormated(datafile, chart_name)

    if 'MAXMIN' in narrative_point:
        cp.max_portrait(datafileFormated)
        cp.min_portrait(datafileFormated)
    if 'CORR' in narrative_point:
        cp.corr_portrait(datafileFormated)
    if 'SMO' in narrative_point:
        cp.SMO_portrait(datafileFormated)
    if 'MONO INTERVAL' in narrative_point:
        cp.Interval_portrait(datafileFormated)
    if 'SLOPESTD' in narrative_point:
        cp.std_portrait(datafileFormated)
        cp.slope_portrait(datafileFormated)
    if 'TOP' in narrative_point:
        cp.Top_portrait(datafileFormated)

pd.DataFrame(cp.chart_summary).to_csv("res.csv", index=False)
pd.DataFrame(cp.chart_summary).to_pickle("res.pkl")



