from collections import OrderedDict,defaultdict
import numpy as np
from itertools import product
import glob
import os
import pandas as pd

#########NEXT SECTION IS ABOUT OWM MODULE
from app.components.charts.ai_lib import MeasureFormater
from .DatafileFormated import DatafileFormated


class interest_point:

    def __init__(self, datafile_path, tagfile_path, prdatafile_path, prtagfile_path):

        self.datafile_path = datafile_path
        self.tagfile_path = tagfile_path
        self.prdatafile_path = prdatafile_path
        self.prtagfile_path = prtagfile_path
        self.measureformater = MeasureFormater.MeasureFormater()
        self.alldatafile = glob.glob(os.path.join(self.datafile_path ,"**", "*.csv"), recursive=True)
        self.alltagfile = glob.glob(os.path.join(self.tagfile_path ,"**", "*.csv"), recursive=True)
        self.interest_score_dict = defaultdict(tuple)

    def top_filter(self, topk):

        for i in range(0, len(self.alldatafile)):
            datafile = pd.read_csv(self.alldatafile[i])
            tagfile = pd.read_csv(self.alltagfile[i])
            datafile = datafile.fillna('0')
            filename = self.alldatafile[i].split('\\')[-1][:-4]
            importanace_score = tagfile['Importance_score'].values[0]
            class_id = tagfile['ClassID'][0]

            if 'X1' not in datafile.columns: #skip picture without X axis.
                pass

            else:
                if datafile.shape[0] - 1 <= topk:

                    tagfile.to_csv(self.prtagfile_path + '\\' + filename + '.csv', index = False)
                    datafile.to_csv(self.prdatafile_path + '\\' + filename + '.csv', index = False)
                    interest_point, interestscore = self.evalutefromdf(datafile,tagfile)
                    self.interest_score_dict[filename] = (interestscore, importanace_score, class_id, interest_point)
                else:
                    for cols in [x for x in datafile.columns if x.startswith('Y')]:
                        interest_level = []
                        Y_tag = datafile[cols][0]
                        filenameT = filename + '_TOP_' + str(topk) + '_' + str(Y_tag)
                        trail_copy = datafile.copy()
                        datafile.loc[1:,cols] = datafile.iloc[1:][cols].astype(float)
                        trail_copy.iloc[1:,] = datafile.iloc[1:,].sort_values(by = cols, ascending=False).values
                        if trail_copy.shape[0] > topk + 1:
                            top_filter = trail_copy.iloc[0:topk + 1,]

                        else:
                            top_filter = trail_copy

                        filter_tagfile = tagfile.copy()

                        for col in [x for x in top_filter.columns if x.startswith('X')]:
                            x_set = set(top_filter[col])
                            filter_tagfile = filter_tagfile[filter_tagfile[col].isin(x_set)]

                        filter_tagfile['TopkFilter'] = 'TOP {} {}'.format(str(topk), str(Y_tag))
                        filter_tagfile.to_csv(self.prtagfile_path + '\\' + filenameT + '.csv', index = False)
                        top_filter.to_csv(self.prdatafile_path + '\\' + filenameT + '.csv', index = False)
                        interest_point, interestscore = self.evalutefromdf(top_filter,filter_tagfile)
                        self.interest_score_dict[filenameT] = (interestscore, importanace_score, class_id, interest_point)



    def evalutefromdf(self, datafile, tagfile, chart_name):
        """
        Evaluate a picture's interest level.
        Input: datafile(for data)
        tagfile(for interest_element)

        Output: interest_level: interest score for various levels
               interest_score: average of interest_level scores.
        """
        datafileFormated = DatafileFormated(datafile, chart_name)
        datafile = datafile.fillna('0')
        interest_element = tagfile['Interest_element'][0]
        interest_level = OrderedDict()

        if 'MAX' in interest_element:
            res = self.measureformater.max(datafileFormated)
            maxscores = [x[-2] for x in res]
            maxmax_ind = np.argmax(maxscores)
            x_name = res[maxmax_ind][0]
            y_name = res[maxmax_ind][1]
            interest_level['MAX'] = [np.max(maxscores),(x_name, y_name)]

        if 'MIN' in interest_element:
            res = self.measureformater.min(datafileFormated)
            minscores = [x[-2] for x in res]
            minmin_ind = np.argmax(minscores)
            x_name = res[minmin_ind][0]
            y_name = res[minmin_ind][1]
            interest_level['MIN'] = [np.max(minscores),(x_name, y_name)]

        if 'CORR' in interest_element:
            res = self.measureformater.correlation(datafileFormated)
            corr_scores = [x[-1] for x in res]
            interest_level['CORRELATION'] = [np.max(corr_scores)]

        if 'SLOPE' in interest_element:
            res = self.measureformater.slope(datafileFormated)
            slope_scores = [x[-1] for x in res]
            interest_level['SLOPE'] = [np.max(slope_scores)]

        if 'STD' in interest_element:
            res = self.measureformater.std(datafileFormated)
            std_scores = [x[-1] for x in res]
            interest_level['STD'] = [np.max(std_scores)]

        if 'MONO INTERVAL' in interest_element:
            res = self.measureformater.interval(datafileFormated)
            len_y = len(res)
            all_combo = list(product(list(range(0,len_y)),[2,5]))
            temp = {}
            for combo in all_combo:
                temp[combo] = res[combo[0]][combo[1] + 2]

            max_interval_key = max(temp, key = temp.get)
            x_name = res[max_interval_key[0]][max_interval_key[1]]
            score = temp[max_interval_key]
            interest_level['MONO INTERVAL'] = [score, x_name]

        if 'SMO' in interest_element:
            res = self.measureformater.smo(datafileFormated)
            score = res[0]
            x = res[1]
            interest_level['SMO'] = [score, x]


        all_interest_metric = np.array([x[0] for x in interest_level.values()])
        interest_score = {'top2mean':np.mean(np.sort(all_interest_metric)[[-1,-2]]), 'mean':np.mean(all_interest_metric)}
        #print(interest_score)
        return interest_level, interest_score


