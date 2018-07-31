from .base_chart import BaseChart
from collections import defaultdict
import pandas as pd

class MultipleLineChart(BaseChart):

    def __init__(self):
        super().__init__()
        self.__type__ = 'line'
        self.__xAxis__ = []
        self.__yAxis__ = {
            "title": "Total percent market share"
        }
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['line', 'table']

    def transformation(self, raw_data):
        # print(raw_data)
        data = raw_data.get('data')
        self._set_common_properties(raw_data)

        xAxis, yAxis = self._parse_header(data)
        x_label, y_label = xAxis[0], yAxis[0]
        if raw_data.get('pivot')[0]:
            xAxis, yAxis = self._parse_header(data)
            groupResult = data.groupby(xAxis[-1]).groups
            result = []
            _xAxis = []
            flag = True
            x2_name = data.loc[0].get('X2')
            y1_name = data.loc[0].get('Y1')

            for key,value in groupResult.items():
                d = []

                if key == x2_name:
                    continue
                for i in value.values:
                    column = data.loc[i]
                    if flag:
                        _xAxis.append(column['X1'])
                    d.append(float(column['Y1']))
                flag = False
                self.__series__.append({'name': key, 'data':d})

            self.__xAxis__ = {'title': 'X1', 'categories':_xAxis}

            self._get_hover_data(_xAxis, raw_data)
        else:
            if data[x_label][0] == 'DATE RANGE':
                self.__xAxis__ = {'categories': self._date_formatter(data[x_label][1:].values), 'title':x_label}
            else:
                self.__xAxis__ = {'categories': data[x_label][1:].values.tolist(), 'title':x_label}
            if len(yAxis) == 0:
                self.__series__.append({"name":data[y_label][0],"data": [float(value) for value in data[y_label][1:].values]})
                self.__highlight__ = self._get_hover_data(self.__xAxis__.get('categories'), raw_data)
            else:
                for count, elem in enumerate(yAxis):
                    self.__series__.append({"name":data[elem][0],"data": [float(value) for value in data[elem][1:].values]})
                    self.__highlight__ = self._get_hover_data_no_pivot(raw_data, data, x_label, count)


    def _get_hover_data(self, xAxis, raw_data):
        if raw_data.get('df_highlights')[0] != True:
            return

        df_highlights = raw_data.get('df_highlights')[1]
        narrative_highlights = raw_data.get('narrative_highlights')[1]

        highlight = []
        hover_data_list = []


        for i in range(len(df_highlights)):

            # print(df_highlights[i], "---", narrative_highlights[i])

            if df_highlights[i].find(narrative_highlights[i]) == -1:
                continue;

            # print(xAxis, " *** ", narrative_highlights[i])
            index = xAxis.index(narrative_highlights[i])
            hover_data_list.append({"group":0, "index":index})

            self.__highlight__.append({"hoverData":hover_data_list, "hoverContent":narrative_highlights[i]})
            break;

    def _get_hover_data_no_pivot(self, raw_data, df, x_label, y_count = 0):
        hover_list = []
        highlight, df_highlights = raw_data['df_highlights']
        _, hover_content = raw_data['narrative_highlights'] 

        if highlight:
            for i in range(len(df_highlights)):
                hover_dic = defaultdict(int)
                hover_data_dic = defaultdict(int)
                hover_data_list = [] 

                group_data=df_highlights[i].split("_")[0]
                value_data=df_highlights[i].split("_")[-1]

                if df[x_label][0] == 'DATE RANGE':
                    group_data_index = 0
                    value_index = self.__xAxis__["categories"].index(value_data)
                else:
                    group_data_index = y_count
                    value_index = self.__xAxis__["categories"].index(value_data)
                # else:
                    # value_index = self.__xAxis__["categories"].index(value_data)
                # value_index = self.__series__[0]["data"].index(value_data)

                hover_data_dic['group'] = group_data_index
                hover_data_dic['index'] = value_index
                hover_data_list.append(hover_data_dic)
                hover_dic['hoverContent'] = hover_content[i]
                hover_dic['hoverData'] = hover_data_list
                hover_list.append(hover_dic)

        return hover_list