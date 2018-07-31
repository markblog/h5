__author__ = 'V631932'

import pandas as pd
import glob
import os
import warnings
warnings.filterwarnings("ignore")

#########NEXT SECTION IS ABOUT OWM MODULE
from .DatafileFormated import DatafileFormated
from .ChartPortraitsWriter import chart_portraits
from .narrative_support import get_file_narratives

class chart_narrative:

    def __init__(self, prdatafile_list, prtagfile_list, percentile_dict_path):

        #self.prdatafile_path = prdatafile_path
        #self.prtagfile_path = prtagfile_path
        #self.alldatafiles = glob.glob(os.path.join(prdatafile_path, "**", "*.csv"), recursive=True)
        #self.alltagfiles = glob.glob(os.path.join(prtagfile_path, "**", "*.csv"), recursive=True)
        #self.allfilenames = [x.split('\\')[-1] for x in self.alltagfiles]
        self.prdatafile_list = prdatafile_list
        self.prtagfile_list = prtagfile_list
        self.cp = chart_portraits(percentile_dict_path)
        self.chart_summary_df = None

    def get_chart_summary(self):

        #for i, filename in enumerate(self.allfilenames):
        for df, tf, filenames in zip(self.prdatafile_list.values(), self.prtagfile_list.values(), self.prdatafile_list.keys()):
            
            narrative_point = list(tf['Narrative_element'])[0]
            datafile = df
            chart_name = filenames 

            datafileFormated = DatafileFormated(datafile, chart_name)

            if 'MAX' in narrative_point:
                self.cp.max_portrait(datafileFormated)
            if 'MIN' in narrative_point:
                self.cp.min_portrait(datafileFormated)
            if 'CORR' in narrative_point:
                self.cp.corr_portrait(datafileFormated)
            if 'SMO' in narrative_point:
                self.cp.SMO_portrait(datafileFormated)
            if 'MONO INTERVAL' in narrative_point:
                self.cp.Interval_portrait(datafileFormated)
            if 'STD' in narrative_point:
                self.cp.std_portrait(datafileFormated)
            if 'SLOPE' in narrative_point:
                self.cp.slope_portrait(datafileFormated)
            if 'TOP' in narrative_point:
                self.cp.Top_portrait(datafileFormated)

        self.chart_summary_df = pd.DataFrame(self.cp.chart_summary)

    def get_all_narrative_and_highlights(self):
        self.get_chart_summary()
        #gfn = get_file_narratives(self.chart_summary_df, self.prtagfile_path)
        narrative_highlight_dict = {}
        for filename in self.prdatafile_list.keys():
            #print(filename)
            gfn = get_file_narratives(self.chart_summary_df, self.prdatafile_list, self.prtagfile_list, filename)
            k = filename
            v = {'narrative':gfn.get_narrative(), 'df_highlights':gfn.get_highlight()[0],
            'narrative_highlights': gfn.get_highlight()[1]}
            narrative_highlight_dict[k] = v

        return narrative_highlight_dict