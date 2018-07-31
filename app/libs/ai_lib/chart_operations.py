from collections import OrderedDict
import numpy as np
import re
import os
from datetime import datetime
import pandas as pd

from functools import lru_cache

class Chartoperation:
    
    # @lru_cache(maxsize=32)
    def __init__(self, date, chart_dict_all='all_charts_dict.pickle', shown_chart_names='all_chart_shown.pickle',
                    single_entity_dict='singleEntityDict_filtered.pickle',
                    cross_entity_dict='crossEntityDict_filtered.pickle',
                    alert_type_all='all_alert_type_dict.pickle',
                    theme_dict = 'themedict.pickle',
                    type_dict = 'typedict.pickle'):

        #date format: '2017_6_22'

        # r = re.compile('.{4}_.{2}')
        # dir_lists = os.listdir()
        # dir_lists_with_date = [x for x in dir_lists if r.match(x)]
        # dir_datetime = [datetime.strptime(x, '%Y_%m') for x in dir_lists_with_date]
        # temp_datetime = datetime.strptime(date, '%Y/%m/%d')
        # mindatetime = min(dir_datetime, key=lambda x: abs(x - temp_datetime))
        # date_folder_name = mindatetime.strftime("%Y_%m")

        # chart_dict_all_path = os.path.join(date_folder_name, chart_dict_all)
        # chart_dict_all = pd.read_pickle(chart_dict_all_path)

        # shown_chart_names_path = os.path.join(date_folder_name, shown_chart_names)
        # shown_chart_names = pd.read_pickle(shown_chart_names_path)

        # single_entity_dict_path = os.path.join(date_folder_name, single_entity_dict)
        # single_entity_dict = pd.read_pickle(single_entity_dict_path)

        # cross_entity_dict_path = os.path.join(date_folder_name, cross_entity_dict)
        # cross_entity_dict = pd.read_pickle(cross_entity_dict_path)

        # theme_dict_path = os.path.join(date_folder_name, theme_dict)
        # theme_dict = pd.read_pickle(theme_dict_path)

        # type_dict_path = os.path.join(date_folder_name, type_dict)
        # type_dict = pd.read_pickle(type_dict_path)

        self.chart_dict_all = chart_dict_all
        self.chart_dict_filtered = OrderedDict()
        for x in shown_chart_names:
            self.chart_dict_filtered[x] = self.chart_dict_all[x]
        #self.chart_dict_filtered = {x: self.chart_dict_all[x] for x in shown_chart_names}
        #print(single_entity_dict.keys())
        #print(cross_entity_dict.keys())
        self.single_entity_dict = single_entity_dict
        self.crossEntityDict = cross_entity_dict
        self.shown_chart_names = shown_chart_names
        self.alert_type_all = alert_type_all
        self.theme_dict = theme_dict
        self.type_dict = type_dict

    def get_alert_by_type(self, alert_type_id):
        return self.alert_type_all[alert_type_id]


    def get_charts_details(self, filename):
        return self.chart_dict_all[filename]
    
    def get_related_charts(self, filename, k):
        """
        params:
            filename: chart name
            k: number of related charts extracted
        return:
            Ordedict {key:Filename, value: chart detail dict}
        """
        related_charts_dict = OrderedDict()
        all_related_charts = self.chart_dict_all[filename]['related_charts']
        
        for i in all_related_charts[0:k]:
            related_charts_dict[i] = self.chart_dict_all[i]

        return related_charts_dict
    
    def get_first_k_charts(self, k):
        length = len(self.chart_dict_filtered)
        if length < k:
            raise Exception('The number of charts required %s excesses the number of charts provided %s' % (length, k))

        first_k_chart = OrderedDict()
        for c in list(self.chart_dict_filtered.keys())[0:k]:
            first_k_chart[c] = self.chart_dict_filtered[c]
        return first_k_chart
    
    def get_charts_by_page(self, chart_base, page_no, page_size=6, level='manager'):
        """
        params:
            page_no:  page number of the charts
            page_size: the number of the charts would give to front end
            chart_base: a list of chart names to be shown
        return:
            Ordedict {key:Filename, value: chart detail dict}
        """
        chart_details = OrderedDict()
        chart_index_start = (page_no - 1) * page_size
        chart_index_end = page_no * page_size
        len_all_chart = len(chart_base)
        total_page_num = int(len_all_chart)    

        if chart_index_start > len_all_chart:
            raise Exception('The number of charts required excesses the number of charts provided')

        if chart_index_end > len_all_chart:
            chart_index_end = len_all_chart

        for i in range(chart_index_start, chart_index_end):
            chart_details[chart_base[i]] = self.chart_dict_all[chart_base[i]]

        return chart_details, total_page_num
        
    
    def get_singleEntitycharts(self, key_entity):
        
        return self.single_entity_dict[key_entity]

    def get_crossEntityfile(self, asset_level):

        return self.crossEntityDict[asset_level]

    def get_themecharts(self, theme):
        # theme in ['performance', 'compliance', 'risk']
        if theme == 'all':
            return self.chart_dict_all.keys()
        else:
            return self.theme_dict[theme]

    def get_typechart(self, type):

        print(type, 'in get_typechart')

        # type in ['COMBINATION', 'COMBINE', 'WATERFALL', 'COLUMN', 'STACKED-COLUMN',
        #  'MULTIPLE-LINE', 'PERCENTAGE-AREA', 'PIE', 'HEAT-MAP', 'GROUP-COLUMN']
        if type in self.type_dict:
            picid = self.type_dict[type]['id']
            print(picid)
            return {picid: self.chart_dict_all[picid]}

        else:
            raise Exception('Chart Type not supported')





if __name__ == '__main__':
#     all_charts_dict_path = 'D:\Fusion_data_final\\savedobject\\all_charts_dict.pickle'
#     all_chart_shown_path = 'D:\Fusion_data_final\\savedobject\\all_chart_shown.pickle'
#     singleEntityDict_filtered_path = 'D:\Fusion_data_final\\savedobject\\singleEntityDict_filtered.pickle'
#     crossEntityDict_filtered_path = 'D:\Fusion_data_final\\savedobject\\crossEntityDict_filtered.pickle'
#     all_alert_type_dict_path = 'D:\Fusion_data_final\\savedobject\\all_alert_type_dict.pickle'
#
#     all_charts_dict = pd.read_pickle(all_charts_dict_path)
#     all_chart_shown = pd.read_pickle(all_chart_shown_path)
#     singleEntityDict_filtered = pd.read_pickle(singleEntityDict_filtered_path)
#     crossEntityDict_filtered = pd.read_pickle(crossEntityDict_filtered_path)
#     all_alert_type_dict = pd.read_pickle(all_alert_type_dict_path)
#
#     chartoperation = Chartoperation(all_charts_dict, all_chart_shown, singleEntityDict_filtered, crossEntityDict_filtered, all_alert_type_dict)
#     a = chartoperation.get_first_k_charts(6)
#     b = chartoperation.get_charts_by_page(all_chart_shown, 1)
#     #print('Total Ranking:', b[0].keys())
#
#     #print(chartoperation.single_entity_dict.keys())
#     #print(chartoperation.cross_entity_dict.keys())
# #
#     list1 = chartoperation.get_singleEntitycharts(1)
#     page1 = chartoperation.get_charts_by_page(list1, 1)
#     # print('Certain Entity Page1 :', page1[0].keys())
#     # print('Certain Entity:', chartoperation.get_singleEntitycharts(1))
#
#     # alert = chartoperation.get_alert_by_type('1')
#     # print(alert)
#
#     list2 = chartoperation.get_crossEntityfile('Asset Class Level 1')
#     page1 = chartoperation.get_charts_by_page(list2, 1)
#
#     print(page1[0].keys())


    #print(s_datetime)
    #print(os.listdir())

    chartoperation = Chartoperation('2017/06/20')
    # print(chartoperation.theme_dict.keys())
    # print(chartoperation.get_typechart('PIE'))
    # print(chartoperation.get_themecharts('asset class level 1'))
    print(chartoperation.chart_dict_all['F00044_all_0_S2BC_PROPTYHG(AC1)_PROPTYHG(AC2)_SUYF'])