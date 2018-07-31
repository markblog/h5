from .base_chart import BaseChart
from collections import defaultdict
import ast

class CombinationChart(BaseChart):
    """

    """

    def __init__(self):
        super().__init__()
        self.__type__ = 'combination'
        self.__description__ = 'combination chart'
        self.__xAxis__ = []
        self.__yAxis__ = []
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['combination', 'table']


    def transformation(self, raw_data):
        # print(raw_data)
        df = raw_data['data']
        self._set_common_properties(raw_data)
        
        y_group = raw_data.get('Y_Group')
        xAxis, yAxis = self._parse_header(df)

        x = xAxis[-1]
        if df[x][0] == 'DATE RANGE':
            self.__xAxis__ = {'categories': self._date_formatter(df[x][1:].values)}
        else:
            self.__xAxis__ = {'categories': df[x][1:].values.tolist()}

        metric_type_dic = self._ymetric_chart_type(y_group)
        for yAxis, y in enumerate(yAxis):
            self.__yAxis__.append({'title':df[y][0]})

            self.__series__.append({
                    'name': df[y][0],
                    'type': metric_type_dic.get(y)['type'],
                    'data': [float(value) for value in df[y][1:].values],
                })


        self.__highlight__= self._get_hover_data(raw_data, df, xAxis)

    def _ymetric_chart_type(self, y_group):

        group_type_data = ast.literal_eval(y_group)

        res = {}
        for index, item in enumerate(group_type_data):
            yAxis = index
            for metric in item.get('YMETRIC'):
                res[metric] = {
                    'type':item.get('TYPE').lower(),
                    'yAxis': yAxis
                }
                if res[metric]['type'] == 'group-column':
                    res[metric]['type'] = 'column'
                
        return res

    def _get_hover_data(self, raw_data, df, x_label, y_count = 0):
        hover_list = []
        highlight, df_highlights = raw_data['df_highlights']
        _, hover_content = raw_data['narrative_highlights'] 

        # print(raw_data)

        if highlight:
            for i in range(len(df_highlights)):
                hover_dic = {}
                hover_data_dic = {}
                hover_data_list = [] 


                group_data=df_highlights[i].split("_")[0]
                value_data=df_highlights[i].split("_")[-1]
                print("*** ", self.__highlight__, " ***")
                group_data_index = 0
                value_index = self.__xAxis__["categories"].index(value_data)
                print("*** ", 1, " ***")
                hover_data_dic['group'] = group_data_index
                hover_data_dic['index'] = value_index
                hover_data_list.append(hover_data_dic)
                hover_dic['hoverContent'] = hover_content[i]
                hover_dic['hoverData'] = hover_data_list
                hover_list.append(hover_dic)

        return hover_list

    def _get_hover_data_(self, raw_data, df, xAxis):

        hover_list = []
        highlight, df_highlights = raw_data['df_highlights']
        _, hover_content = raw_data['narrative_highlights'] 

        if highlight:
            hover_dic = {}
            hover_data_dic = {}
            hover_data_list = []

            hover_data_dic['group'] = 0
            print(222222222222222222)
            hover_data_dic['index'] = self._get_hover_index(df, df_highlights, xAxis)
            print(333333)
            hover_data_list.append(hover_data_dic)
            hover_dic['hoverContent'] = hover_content[0]
            hover_dic['hoverData'] = hover_data_list
            hover_list.append(hover_dic)

        return hover_list

    def _get_hover_index(self, df, highlights, xAxis):

        labels_combination = '_'.join([highlight.split('_')[-1] for highlight in highlights])
        _df = df[xAxis[0]]
        for x in xAxis[1:]:
            _df = _df + '_' + df[x]
        return _df.values.tolist().index(labels_combination) - 1