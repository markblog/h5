import numpy as np

#########NEXT SECTION IS ABOUT OWM MODULE
from . import Measure
from . import Normalizer
import pickle

class Sampler:

    #with_sample = False

    def __init__(self, percentile_dict_path):

        self.percentile = [5, 10, 20, 35, 50, 65, 80, 90, 95]
        self.percentile_CORRELATION = [-0.94, -0.8, -0.53, -0.23, -0.07, 0.0015, 0.024, 0.087, 0.31]
        with open(percentile_dict_path, 'rb') as handle:
            self.thresh_dict = pickle.load(handle)

    def get_closest_number(self, mylist, mynumber):

        return min(mylist, key = lambda x: np.abs(x - mynumber))

    def maxminsampler(self, length):
        # if with_sample:
        #     all_samples = []
        #     for _ in range(0, 10000):
        #         data_list = np.random.randn(length)
        #         max_num = np.max(data_list)
        #         all_samples.append(max_num)
        #
        #     percentile = [np.percentile(all_samples, p) for p in self.percentile]
        #     return percentile
        # else:
        #     return [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        maxmin_dict = self.thresh_dict['MAXMIN']
        number_list = list(maxmin_dict.keys())
        closest_number = self.get_closest_number(number_list, length)

        return maxmin_dict[closest_number]


    def sum_outlier_sampler(self, length, ny):
        # if with_sample:
        #     all_res = []
        #     for _ in range(1000):
        #         yi = np.array([0.0] * length)
        #         for i in range(ny):
        #             yi += np.abs(np.random.randn(length))
        #
        #         all_res.append(np.max(yi))
        #
        #     percentile = [np.percentile(all_res, i) for i in self.percentile]
        #     return percentile
        # else:
        #     return [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        smo_dict = self.thresh_dict['SMO']
        number_tuple = list(smo_dict.keys())
        number_list_length = list(set([x[0] for x in number_tuple]))
        number_list_ny = list(set([x[1] for x in number_tuple]))
        closest_number_length = self.get_closest_number(number_list_length, length)
        closest_number_ny = self.get_closest_number(number_list_ny, ny)

        return smo_dict[(closest_number_length, closest_number_ny)]


    def outlier_sampler(self, nd):
        # if with_sample:
        #     all_res = []
        #     for _ in range(1000):
        #         yi = np.abs(np.random.randn(nd))
        #         all_res.append(yi)
        #     percentile = [np.percentile(all_res, i) for i in self.percentile]
        #     return percentile
        # else:
        #     return [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        out_dict = self.thresh_dict['OUT']
        number_list = list(out_dict.keys())
        closest_number = self.get_closest_number(number_list, nd)

        return out_dict[closest_number]

    def ts_amount_length_sampler(self, length):
        # if with_sample:
        #     def get_AR1(n):
        #         series = []
        #
        #         beta_0 = np.random.randn() / 2
        #         beta_1 = np.random.randn() / 2
        #         x = np.random.randn() + 10
        #
        #         series.append(x)
        #         for _ in range(1, n):
        #             x = x * beta_1 + beta_0 + np.random.randn() * 2
        #             series.append(x)
        #
        #         return series
        #
        #     amount = []
        #     interval = []
        #     measure_calculator = Measure.Measure()
        #
        #     for _ in range(10000):
        #         ar1 = get_AR1(length)
        #         """
        #          return [[max(relative_change), abs(min(relative_change))]\
        #          , [max(change_len), abs(min(change_len))] \
        #          , [max(change_vol), min(change_vol)] \
        #          , [pos_relative_change_interval, neg_relative_change_interval],
        #            [longest_increase_interval, longest_decrease_interval]]
        #         """
        #         res = measure_calculator.max_interval_change(ar1)
        #         if res[0] in ["Increasing", "Decreasing"]:
        #             continue
        #         increase, decrease, interval_1, interval_2 = res[0][0], res[0][1], res[1][0], res[1][1]
        #         amount.append(increase)
        #         amount.append(decrease)
        #         interval.append(interval_1)
        #         interval.append(interval_2)
        #
        #     percentile_amount = [np.percentile(amount, i) for i in self.percentile]
        #     percentile_length = [np.percentile(interval,i) for i in self.percentile]
        #
        #     return percentile_amount, percentile_length
        # else:
        #     return [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        interval_dict = self.thresh_dict['INTERVAL']
        number_list = list(interval_dict.keys())
        closest_number = self.get_closest_number(number_list, length)

        return interval_dict[closest_number]



    def slope_sampler(self, length):
        # if with_sample:
        #
        #     def get_AR1(n):
        #         series = []
        #
        #         beta_0 = np.random.randn() / 2
        #         beta_1 = np.random.randn() / 2
        #         x = np.random.randn() + 10
        #
        #         series.append(x)
        #         for _ in range(1, n):
        #             x = x * beta_1 + beta_0 + np.random.randn() * 2
        #             series.append(x)
        #
        #         return series
        #     slope = []
        #     measure_calculator = Measure.Measure()
        #     for _ in range(10000):
        #         ar1 = get_AR1(length)
        #         slope.append(abs(measure_calculator.slope(ar1)))
        #     percentile = [np.percentile(slope, i) for i in self.percentile]
        #     return percentile
        #
        # else:
        #     return [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        slope_dict = self.thresh_dict['SLOPE']
        number_list = list(slope_dict.keys())
        closest_number = self.get_closest_number(number_list, length)

        return slope_dict[closest_number]



    def std_sampler(self, length):
        # if with_sample:
        #     std_dist = []
        #     sc = Normalizer.Normalizer()
        #
        #     for _ in range(0, length):
        #         rand_list = np.random.randn(length)
        #         rand_list_transform = sc.maxmin(rand_list)
        #         std = np.std(rand_list_transform)
        #         std_dist.append(std)
        #     percent = [np.percentile(std_dist, p) for p in self.percentile]
        #
        #     return percent
        # else:
        #     return [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        std_dict = self.thresh_dict['STD']
        number_list = list(std_dict.keys())
        closest_number = self.get_closest_number(number_list, length)

        return std_dict[closest_number]


class Score:

    def __init__(self, percentile_dict_path):

        self.sampler = Sampler(percentile_dict_path)
        self.with_sample = False

    def get_score(self,score):
        if len(score) < 1:
            return np.nan
        else:
            return max(score)
        return score

    def maxminscore(self, value, length):
        value = np.abs(value)
        percentile = self.sampler.maxminsampler(length)
        #print(percentile)
        score = np.where(np.sort(percentile + [value]) == value)[0] + 1
        #print(np.sort(percentile + [value]))
        return self.get_score(score)

    def smoscore(self,value,length,ny):
        percentile = self.sampler.sum_outlier_sampler(length,ny)
        score = np.where(np.sort(percentile + [value]) == value)[0] + 1
        return self.get_score(score)

    def outliarscore(self,value,length):
        percentile = self.sampler.outlier_sampler(length)
        score = np.where(np.sort(percentile + [value]) == value)[0] + 1
        return self.get_score(score)

    def slope(self,value,length):
        value = abs(value)
        percentile = self.sampler.slope_sampler(length)
        score = np.where(np.sort(percentile + [value]) == value)[0] + 1
        return self.get_score(score)


    def ts_amount_length_score(self, rcs, cls, length):
        percentile_amount, percentile_length = self.sampler.ts_amount_length_sampler(length)
        increase_amount_score = np.argwhere(np.sort(list(percentile_amount) + [rcs[0]]) == rcs[0])[0] + 1
        decrease_amount_score = np.argwhere(np.sort(list(percentile_amount) + [rcs[1]]) == rcs[1])[0] + 1
        increase_len_score = np.argwhere(np.sort(list(percentile_length) + [cls[0]]) == cls[0])[0] + 1
        decrease_len_score = np.argwhere(np.sort(list(percentile_length) + [cls[1]]) == cls[1])[0] + 1
        return [increase_amount_score,decrease_amount_score, increase_len_score,decrease_len_score]

    def mincorr_score(self, value):
        return self.get_score(10 - np.where(np.sort(self.sampler.percentile_CORRELATION + [value]) == value)[0])

    def std_score(self, value, length):

        percentile = self.sampler.std_sampler(length)

        score = np.where(np.sort(percentile + [value]) == value)[0] + 1

        return score[0]


if __name__=="__main__":
    sc = Score()
    sp = Sampler()
    #print(sp.thresh_dict)
    print(sc.maxminscore(3, 10), sc.maxminscore(-3, 10))
    print(sc.smoscore(3, 10, 2))
    print(sc.outliarscore(3, 10), sc.outliarscore(5, 10))
    print(sc.slope(3, 10), sc.slope(5, 10))
    #print(sc.ts_amount_length_score(3, 10), sc.ts_amount_length_score(5, 10))
    print(sc.std_score(0.1, 10), sc.std_score(5, 10))
