from .base_chart import BaseChart
from collections import defaultdict
import ast

class CombineChart(BaseChart):
    """
    CombineChart is the class of delivering the chart with different type of chars linking together

    """

    def __init__(self):
        super().__init__()
        self._default_type = ['column','line']
        self.__type__ = 'combine'
        self.__xAxis__ = []
        self.__yAxis__ = []
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['combine', 'table']


    def transformation(self, raw_data):
        # print(raw_data)

        df = raw_data['data']
        self._set_common_properties(raw_data)
        
        y_group = raw_data.get('Y_Group')
        y_group = ast.literal_eval(y_group)
        xAxis, yAxis = self._parse_header(df)

        x = xAxis[-1]
        if df[x][0] == 'DATE RANGE':
            self.__xAxis__.append({'categories': self._date_formatter(df[x][1:].values)})
        else:
            self.__xAxis__.append({'categories': df[x][1:].values.tolist()})

        metric_type_dic = self._ymetric_chart_type(y_group)
        if raw_data.get('type').lower() == 'combine':
            self.__yAxis__ = [{'title':'placeholder'},{'title':'placeholder'}]
        else:
            self.__yAxis__ = [{'title':'placeholder'}]

        for yAxis, y in enumerate(yAxis):

            if raw_data.get('type').lower() == 'combine':
                self.__series__.append({
                        'name': df[y][0],
                        'type': metric_type_dic.get(y)['type'],
                        'data': [float(value) for value in df[y][1:].values],
                        'yAxis': metric_type_dic.get(y)['yAxis']
                    })
            else:
                self.__series__.append({
                        'name': df[y][0],
                        'type': metric_type_dic.get(y)['type'],
                        'data': [float(value) for value in df[y][1:].values]
                    })


        self.__highlight__ = self._get_hover_data(raw_data, df, xAxis)

    def _ymetric_chart_type(self, group_type_data):

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
                # if df[x_label][0] == 'DATE RANGE':
                #     print("*** ", self.__xAxis__["categories"], " ***", value_data)
                #     group_data_index = 0
                #     value_index = self.__xAxis__["categories"].index(value_data)
                # else:
                group_data_index = y_count
                value_index = self.__xAxis__[0].get("categories").index(value_data)
                hover_data_dic['group'] = group_data_index
                hover_data_dic['index'] = value_index
                hover_data_list.append(hover_data_dic)
                hover_dic['hoverContent'] = hover_content[i]
                hover_dic['hoverData'] = hover_data_list
                hover_list.append(hover_dic)

        return hover_list

    def _get_hover_data_(self, raw_data, df, xAxis):

        highlight, df_highlights = raw_data['df_highlights']
        _, hover_content = raw_data['narrative_highlights']

        if highlight:
            hover_dic = {}
            hover_data_dic = {}
            hover_data_list = []

            hover_data_dic['group'] = 0
            hover_data_dic['index'] = self._get_hover_index(df, df_highlights, xAxis)
            hover_data_list.append(hover_data_dic)
            hover_dic['hoverContent'] = hover_content[0]
            hover_dic['hoverData'] = hover_data_list
            self.__highlight__.append(hover_dic)

    def _get_hover_index(self, df, highlights, xAxis):

        labels_combination = '_'.join([highlight.split('_')[-1] for highlight in highlights])
        _df = df[xAxis[0]]
        for x in xAxis[1:]:
            _df = _df + '_' + df[x]
        return _df.values.tolist().index(labels_combination) - 1




