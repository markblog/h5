__author__ = 'V631932'
"""

Input:

     thresh_dict_path: the path of a dictionary containing the default threshold of alerts. Measure Names(ROR, PERIOD VALUE ADD, CTR) as key, threshold of different period as values.
     prdatafile_list: the datafile dictionary.
     prtagfile_list: the tagfile dictionary.


Main methods:

     get_alert_dict: return the bool of a chart has alert or not,  and the threshold of the alert.
     get_alert_bool_narrative: return a dictionary containing the statement of alert and the narrative of alret.
     get_alert_bool: return the bool of alert or not.
     get_alert_narrative_dic: return the narrative of alert.
     get_custom_alert: get customized alert dictionary.
     get_custom_alert_bool_narrative: get customized alert statement and narrative.

"""

import glob
import os
from collections import OrderedDict
import pandas as pd
import numpy as np
import pickle

class chart_alert:

    def __init__(self, thresh_dict_path, prdatafile_list, prtagfile_list):

        self.thresh_dict_path = thresh_dict_path
        self.prdatafile_list = prdatafile_list
        self.prtagfile_list = prtagfile_list
        with open(self.thresh_dict_path, 'rb') as handle:
            self.thresh_dict = pickle.load(handle)

    def get_alert_dict(self, measure, thresh_dict, prdatafile_list, prtagfile_list):

        alert_dict = {}
        for period in thresh_dict[measure]:
            for chart_id, df in prtagfile_list.items():
                if measure in list(prtagfile_list[chart_id].iloc[0]):
                    for column in df:
                        if "Period" in df[column].unique():
                            if period in df[column].unique():
                                for column in prdatafile_list[chart_id]:
                                    if measure in prdatafile_list[chart_id][column].unique():
                                        ror_arr = np.array(prdatafile_list[chart_id][column].ix[1:]).astype(np.float64)
                                        alert_bool = ror_arr > thresh_dict[measure][period]
                                        alert_dict.update({chart_id: [alert_bool, thresh_dict[measure][period]]})
        return alert_dict

    def get_alert_bool_narrative(self):
        alert = {}
        alert_bool_dict = {}
        alert_narrative_dict = {}
        for chart_id in self.prdatafile_list:
            alert_bool_dict[chart_id] = []
            alert_narrative_dict[chart_id] = []
            alert[chart_id] = {'BOOL': False, 'NARRATIVE': []}
        for measure in self.thresh_dict:
            alert_dict = self.get_alert_dict(measure, self.thresh_dict, self.prdatafile_list, self.prtagfile_list)
            alert_bool_dict_single = self.get_alert_bool(alert_dict)
            for chart_id in alert_bool_dict_single:
                alert[chart_id]['BOOL'] = np.bool(alert[chart_id]['BOOL'] + alert_bool_dict_single[chart_id])
            alert_narrative_dic_single = self.get_alert_narrative_dic(measure, alert_dict)
            for chart_id in alert_narrative_dic_single:
                alert[chart_id]['NARRATIVE'].append(alert_narrative_dic_single[chart_id])

        return alert

    def get_alert_bool(self, alert_dict):
        alert_bool_dict = {}
        for k, v in alert_dict.items():
            if True in v[0]:
                alert_bool_dict[k] = True
            else:
                alert_bool_dict[k] = False
        return alert_bool_dict

    def get_alert_narrative_dic(self, measure, alert_dict):
        alert_narrative_dict = {}
        for k, v in alert_dict.items():
            if True in v[0]:
                alert_narrative_dict[k] = ('{} is over threshold({})'.format(measure, v[1]))
            else:
                pass
        return alert_narrative_dict

    def get_custom_alert(self, measure, df, custom_alert_dict):
        alert_dict = {}
        chart_id = list(custom_alert_dict.keys())[0]
        measure_thresh = list(custom_alert_dict.values())[0]
        for column in df:
            if measure in df[column].unique():
                ror_arr = np.array(df[column].ix[1:]).astype(np.float64)
                alert_bool = ror_arr > measure_thresh[measure]
                alert_dict.update({chart_id: [alert_bool, measure_thresh[measure]]})
        return alert_dict

    def get_custom_alert_bool_narrative(self, df, custom_alert_dict):
        """

        :param df: the dataframe of the chart need alert.
        :param custom_alert_dict: customized alert dictionary. For instance, custom_alert_dict = {'P00004_ALL_.csv': {'NET CASH FLOWS': 4000000, "ROR": 1}}.
        :return: a dictionary containing the statement of the chart has alert or not, and the narrative of alert.
        """

        alert = {}
        alert_bool_dict = {}
        alert_narrative_dict = {}
        chart_id = list(custom_alert_dict.keys())[0]
        chart_thresh = list(custom_alert_dict.values())[0]

        alert_bool_dict[chart_id] = []
        alert_narrative_dict[chart_id] = []
        alert[chart_id] = {'BOOL': False, 'NARRATIVE': []}
        for measure in chart_thresh:
            alert_dict = self.get_custom_alert(measure, df, custom_alert_dict)
            alert_bool_dict_single = self.get_alert_bool(alert_dict)
            for chart_id in alert_bool_dict_single:
                alert[chart_id]['BOOL'] = np.bool(alert[chart_id]['BOOL'] + alert_bool_dict_single[chart_id])
            alert_narrative_dic_single = self.get_alert_narrative_dic(measure, alert_dict)
            for chart_id in alert_narrative_dic_single:
                alert[chart_id]['NARRATIVE'].append(alert_narrative_dic_single[chart_id])

        return alert

if __name__ == "__main__":
    path_thresh_dict = 'D:/project/AI_Chart/LATEST/AI_CODE/data_csvfiles/thresh_dict.pickle'
    prdatafile_path = 'D:/project/AI_Chart/LATEST/AI_CODE/data_csvfiles/PR_datafiles'
    prtagfile_path = 'D:/project/AI_Chart/LATEST/AI_CODE/data_csvfiles/PR_tagfiles'

    tfl = glob.glob(os.path.join(prtagfile_path, "**", "*.csv"), recursive=True)
    prtagfile_list = OrderedDict()
    for x in tfl:
        prtagfile_list[x.split("\\")[-1].split('.')[0]] = pd.read_csv(x)

    dfl = glob.glob(os.path.join(prdatafile_path, "**", "*.csv"), recursive=True)
    prdatafile_list = OrderedDict()
    for x in dfl:
        prdatafile_list[x.split("\\")[-1].split('.')[0]] = pd.read_csv(x)

    abn = chart_alert(path_thresh_dict, prdatafile_list, prtagfile_list)
    # alert_dict = abn.get_alert_bool_narrative()
    # print(alert_dict)
    # print(len(alert_dict))
    # count = 0
    # for k, v in alert_dict.items():
    #     if v['BOOL'] is True:
    #         count += 1
    #         print(k, v)
    # print(count)

    # df = list(prdatafile_list.values())[0]
    custom_alert_dict = {'P00004_ALL_.csv': {'NET CASH FLOWS': 4000000, "ROR": 1}}
    # custom_alert = abn.get_custom_alert_bool_narrative(df, custom_alert_dict)
    # print(custom_alert)

    print(abn.thresh_dict)
