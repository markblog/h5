
import numpy as np
import itertools

#########NEXT SECTION IS ABOUT OWM MODULE
from .DatafileFormated import DatafileFormated
from app.components.charts.ai_lib import Score
from .Normalizer import Normalizer




class Measure:

    def max(self,data):
        return np.max(data), np.argmax(data)

    def min(self,data):
        return np.min(data), np.argmin(data)

    def correlation(self, y1, y2):
        return np.corrcoef(y1,y2)[0,1]

    def sum_outlier(self, array_list):

        res = np.array([0.0] * len(array_list[0]))
        for array in array_list:
            mean = np.mean(array)
            std = np.std(array) + 1e-10
            temp = np.array([abs(x - mean) / std for x in array])
            res += temp

        sum_out_index = np.argmax(res)
        sum_out_res = np.max(res)
        # sum_out_score = sampler.sum_outlier_sampler(np.max(res), len(array_list[0]), len(array_list))
        # y_pos = []
        # y_neg = []
        # y_index = -1
        # for array in array_list:
        #     y_index += 1
        #     mean = np.mean(array)
        #     std = np.std(array) + 1e-10
        #     diff = np.abs(array[sum_out_index] - mean) / std
        #     score = sampler.outlier_sampler(diff, len(array))
        #     if score > 5:
        #         if array[sum_out_index] - mean > 0:
        #             y_pos.append(y_index)
        #         else:
        #             y_neg.append(y_index)
        return [sum_out_res,sum_out_index]




class InterestScoreFormater:
    normalizer = Normalizer()
    score = Score.Score()
    measure = Measure()

    def maxmax(self, datafileFormated):

        names = []
        values = []

        for Y in (datafileFormated.Y_cols):

            data = datafileFormated.get_data(Y)
            max_value, max_index = self.measure.max(data)
            y_name = datafileFormated.get_name(Y)
            x_name = datafileFormated.get_x_name(max_index)
            values.append(max(self.normalizer.difdivstd(data)))
            names.append([x_name, y_name])

        max_value, index = self.measure.max(values)
        maxmaxscore = self.score.maxminscore(max_value, datafileFormated.num_elements)

        return [names[index], maxmaxscore]

    def minmin(self, datafileFormated):

        names = []
        values = []

        for Y in (datafileFormated.Y_cols):

            data = datafileFormated.get_data(Y)
            min_value, min_index = self.measure.min(data)
            y_name = datafileFormated.get_name(Y)
            x_name = datafileFormated.get_x_name(min_index)
            values.append(min(self.normalizer.difdivstd(data)))
            names.append([x_name, y_name])

        min_value, index = self.measure.min(values)
        minminscore = self.score.maxminscore(min_value, datafileFormated.num_elements)

        return [names[index], minminscore]

    def mincorr_score(self, datafileFormated):

        correlation_dict = {}
        y_to_names = {}
        y_cols = datafileFormated.Y_cols
        for i in y_cols:
            y_to_names[i] = datafileFormated.get_name(i)

        all_combo = list(itertools.combinations(y_cols, 2))
        all_combo_name = [(y_to_names[i[0]], y_to_names[i[1]]) for i in all_combo]

        for i, names in enumerate(all_combo_name):
            correlation_dict[names] = self.measure.correlation(datafileFormated.get_data(all_combo[i][0]),
                                                              datafileFormated.get_data(all_combo[i][1]))

        min_key = min(correlation_dict, key=correlation_dict.get)
        min_value = self.score.mincorr_score(correlation_dict[min_key])

        return [min_key, min_value]

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
        return [x_name, score]