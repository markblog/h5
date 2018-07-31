import numpy as np

class Measure:

    def max(self,data):
        return np.max(data), np.argmax(data)

    def min(self,data):
        return np.min(data), np.argmin(data)

    def slope(self,data):
        return (data[-1] - data[0]) / len(data)

    def sum_outlier(self,array_list):

        res = np.array([0.0] * len(array_list[0]))
        for array in array_list:
            mean = np.mean(array)
            std = np.std(array) + 1e-10
            temp = np.array([abs(x - mean) / std for x in array])
            res += temp

        sum_out_index = np.argmax(res)
        sum_out_res = np.max(res)
        return [sum_out_res,sum_out_index]

    def max_interval_change(self,num_array):

        def find_interval_SE(index):
            start = 0
            end = 1
            count = 0
            for i in range(0, len(change_point)):
                if change_point[i]:
                    count += 1
                    if count == index + 1:
                        end = i - 1
                    if count == index:
                        start = i - 1
            if end < start:
                end = len(change_point) - 1
            return [start, end]
        # [1,2,3,4,3,2,1]
        diff_1 = list(np.diff(num_array, 1))
        diff_1.insert(0, 0) #[0,1,1,1,-1,-1,-1]
        change_point = []

        for i in range(0, len(diff_1)):
            if i == 0:
                direction = (diff_1[i + 1] > 0) - 0.5
                change_point.append(False)
            else:
                if diff_1[i] * direction < 0:
                    change_point.append(True)
                    direction = -direction
                else:
                    change_point.append(False)
                    # [False,False,False,False,True,False,False]
        if True not in change_point:

            if np.sum(diff_1) > 0:
                return ["Increasing", [num_array[-1] - num_array[0]]]
            else:
                return ["Decreasing", [num_array[-1] - num_array[0]]]

        change_vol = []
        cur_sum = 0
        change_len = []
        cur_len = -1
        for i in range(0, len(change_point)):
            if change_point[i]:
                change_len.append(cur_len * ((cur_sum > 0) - 0.5) * 2)
                change_vol.append(cur_sum)
                cur_sum = diff_1[i]
                cur_len = 1
            else:
                cur_sum += diff_1[i]
                cur_len += 1

        change_vol.append(cur_sum)
        change_len.append(cur_len * ((cur_sum > 0) - 0.5) * 2)
        # change_vol = [3,-3]
        change_range = max(num_array) - min(num_array)

        relative_change = []
        for i in change_vol:
            temp = change_vol.copy()
            temp.remove(i)
            mean = sum(np.abs(temp)) / (len(change_vol) - 1)
            relative_change.append(i / mean)

        index_pos = np.argmax(relative_change)
        pos_relative_change_interval = find_interval_SE(index_pos)

        index_neg = np.argmin(relative_change)
        neg_relative_change_interval = find_interval_SE(index_neg)

        index_pos_length = np.argmax(change_len)
        longest_increase_interval = find_interval_SE(index_pos_length)

        index_neg_length = np.argmin(change_len)
        longest_decrease_interval = find_interval_SE(index_neg_length)

        return [[max(relative_change), abs(min(relative_change))]\
             , [max(change_len), abs(min(change_len))] \
             , [pos_relative_change_interval, neg_relative_change_interval],
               [longest_increase_interval, longest_decrease_interval]]

    def correlation(self, y1, y2):
        return np.corrcoef(y1,y2)[0,1]

    def top(self,data, percent):
        data = np.array(data)

        positive = data[data > 0]
        negative = data[data < 0]

        positive = -np.sort(-positive)
        negative = np.sort(negative)

        length_pos = int(np.floor(len(positive) * percent))
        length_neg = int(np.floor(len(negative) * percent))

        if length_pos != 0:
            pos_sum_percent = np.sum(positive[0:length_pos + 1]) / np.sum(positive)
        else:
            pos_sum_percent = None

        if length_neg != 0:
            neg_sum_percent = np.sum(negative[0:length_neg + 1]) / np.sum(negative)
        else:
            neg_sum_percent = None

        return [pos_sum_percent, length_pos, neg_sum_percent, length_neg]