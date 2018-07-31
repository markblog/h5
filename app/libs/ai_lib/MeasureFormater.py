import numpy as np
import itertools
import pandas as pd

#########NEXT SECTION IS ABOUT OWM MODULE
from .DatafileFormated import DatafileFormated
from . import Score
from .Normalizer import Normalizer
from . import Measure


class MeasureFormater:


    def __init__(self, percentile_dict_path):

        self.normalizer = Normalizer()
        self.score = Score.Score(percentile_dict_path)
        self.measure = Measure.Measure()

    def max(self, datafileFormated):
        res = []
        for Y in (datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            max_value, max_index = self.measure.max(data)
            y_name = datafileFormated.get_name(Y)
            x_name = datafileFormated.get_x_name(max_index)
            score = self.score.maxminscore(max(self.normalizer.difdivstd(data)), len(data))
            res.append([x_name,y_name,score,max_value])
        return res

    def min(self, datafileFormated):
        res = []
        for Y in (datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            min_value, min_index = self.measure.min(data)
            y_name = datafileFormated.get_name(Y)
            x_name = datafileFormated.get_x_name(min_index)
            score = self.score.maxminscore(min(self.normalizer.difdivstd(data)), len(data))
            res.append([x_name,y_name,score,min_value])
        return res

    def slope(self,datafileFormated):
        res = []
        date =  datafileFormated.get_date()
        for Y in (datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            normed_data = self.normalizer.difdivstd(data)
            start_date = date[0]
            end_date = date[-1]
            slope_val = self.measure.slope(normed_data)
            score = self.score.slope(slope_val,datafileFormated.length)
            res.append([start_date, end_date, datafileFormated.get_name(Y), slope_val, score])
        return res

    def smo(self,datafileFormated):

        normed_sum = None
        Y_score = []

        for Y in (datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            normed_data = self.normalizer.difdivstd(data)
            if normed_sum is not None:
                normed_sum += np.abs(normed_data)
            else:
                normed_sum = np.abs(normed_data)

        max_value, index = self.measure.max(normed_sum)
        length = len(normed_data)

        for Y in (datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            normed_data = self.normalizer.difdivstd(data)
            value = normed_data[index]
            Y_score.append(self.score.outliarscore(value,length) * ((value > 0) - 0.5) * 2)

        score = self.score.smoscore(max_value, len(normed_sum), datafileFormated.num_y)

        x_name = datafileFormated.get_x_name(index)

        y_pos_name = []
        y_neg_name = []
        for i in range(0,len(Y_score)):
            if abs(Y_score[i]) > 5:
                if Y_score[i] > 0:
                    y_pos_name.append(datafileFormated.y_names[i])
                else:
                    y_neg_name.append(datafileFormated.y_names[i])
        return [score, x_name, y_pos_name, y_neg_name]


    def interval(self, datafileFormated):

        res = []
        for Y in(datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            temp = self.measure.max_interval_change(data)
            if temp[0] in ["Increasing", "Decreasing"]:
                #["monotony tag", "Y name", "amount"]
                res.append([temp[0], datafileFormated.get_name(Y),[data[0],data[-1]]])
            else:
                max_relative_change, max_monotony_length,\
                max_change_interval, max_length_interval = temp[0],temp[1],temp[2],temp[3]
                 #    return [[max(relative_change), abs(min(relative_change))]\
                 # , [max(change_len), abs(min(change_len))] \
                 # , [max(change_vol), min(change_vol)] \
                 # , [pos_relative_change_interval, neg_relative_change_interval],
                 #   [longest_increase_interval, longest_decrease_interval]]

                increase_amount_interval_x = [datafileFormated.get_x_name(x) for x in max_change_interval[0]]
                decrease_amount_interval_x = [datafileFormated.get_x_name(x) for x in max_change_interval[1]]
                increaseamount_amount = [data[max_change_interval[0][0]], data[max_change_interval[0][1]]]
                decreaseamount_amount = [data[max_change_interval[1][0]], data[max_change_interval[1][1]]]

                increase_len_interval_x = [datafileFormated.get_x_name(x) for x in max_length_interval[0]]
                decrease_len_interval_x = [datafileFormated.get_x_name(x) for x in max_length_interval[1]]
                increaseamount_len = [data[max_length_interval[0][0]], data[max_length_interval[0][1]]]
                decreaseamount_len = [data[max_length_interval[1][0]], data[max_length_interval[1][1]]]


                increaseinterval_amount_score,decreaseinterval_amount_score\
                ,increaseinterval_length_score,decreaseinverval_length_score = self.score.ts_amount_length_score(max_relative_change,max_monotony_length,datafileFormated.length)
                #["monotony_tag","Y",
                # "maxincrease_interval","increase_amount","increase_score"
                #  maxdecresae_interval, "decrase_len","decrease_score"
                #  maxLENincrease_inverval","increase_amount"(len),"len_score"
                #  maxlendecrease_interval,"decresese_amount","len_socre"
                res.append(["Normal",datafileFormated.get_name(Y)
                            ,increase_amount_interval_x,increaseamount_amount,increaseinterval_amount_score[0]
                            ,decrease_amount_interval_x,decreaseamount_amount,decreaseinterval_amount_score[0]
                            ,increase_len_interval_x,increaseamount_len,increaseinterval_length_score[0]
                            ,decrease_len_interval_x,decreaseamount_len,decreaseinverval_length_score[0]])
        return res


    def correlation(self, datafileFormated):

        corr_list = []
        correlation_dict = {}
        y_to_names = {}
        y_cols = datafileFormated.Y_cols
        for i in y_cols:
            y_to_names[i] = datafileFormated.get_name(i)

        all_combo = list(itertools.combinations(y_cols, 2))
        all_combo_name = [(y_to_names[i[0]], y_to_names[i[1]]) for i in all_combo]

        for i, names in enumerate(all_combo_name):

            value = self.measure.correlation(datafileFormated.get_data(all_combo[i][0]),
                                                              datafileFormated.get_data(all_combo[i][1]))
            temp = [names[0], names[1], value, self.score.mincorr_score(value)]
            corr_list.append(temp)

        return corr_list


    def std(self, datafileFormated):

        res = []
        for Y in (datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            y_name = datafileFormated.get_name(Y)
            scaled_value = Normalizer().maxmin(data)
            std = np.std(scaled_value)
            score = self.score.std_score(std, len(data))
            res.append([y_name, score])
        return res

    def top(self, datafileFormated):
        res = []

        for Y in(datafileFormated.Y_cols):
            data = datafileFormated.get_data(Y)
            temp = self.measure.top(data,0.3)
            data = pd.DataFrame(data)
            data = data.sort_values(0)
            index = data.index

            x_pos = []
            x_neg = []
            for i in range(1, temp[1] + 1):
                x_pos.append(datafileFormated.get_x_name(index[-i]))

            for i in range(0, temp[3]):

                x_neg.append(datafileFormated.get_x_name(index[i]))

            res.append([datafileFormated.get_name(Y), x_pos, temp[0], x_neg, temp[2]])

        return res

