from app.ext import db
from collections import OrderedDict
from .base_chart import BaseChart

class ColumnChart(BaseChart):
    """
    ColumnChart is the class of providing the column basic information! 

    """

    def __init__(self):
        super().__init__()
        self.__type__ = 'column'
        # self.__description__ = 'column chart'
        self.__xAxis__ = []
        self.__yAxis__ = {
            "title": "column chart"
        }
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['column','table']

    def transformation(self, raw_data):
        # print(raw_data)
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)
        x_label, y_label = xAxis[0], yAxis[0]
        if df[x_label][0] == 'DATE RANGE':
            self.__xAxis__ = {'categories': self._date_formatter(df[x_label][1:].values), 'title':x_label}
        else:
            self.__xAxis__ = {'categories': df[x_label][1:].values.tolist(), 'title':x_label}

        if len(yAxis) == 0:
            self.__series__.append({"name":df[y_label][0],"data": [float(value) for value in df[y_label][1:].values]})
            self.__highlight__ = self._get_hover_data(raw_data, df, x_label)
        else:
            for index, elem in enumerate(yAxis):
                # print("*** ", index, " --- ", elem, " ***")
                self.__series__.append({"name":df[elem][0],"data": [float(value) for value in df[elem][1:].values]})
                self.__highlight__ = self._get_hover_data(raw_data, df, x_label, index)

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
                if df[x_label][0] == 'DATE RANGE':
                    group_data_index = 0
                    value_index = self.__xAxis__["categories"].index(value_data)
                else:
                    group_data_index = y_count
                    value_index = self.__xAxis__["categories"].index(value_data)

                hover_data_dic['group'] = group_data_index
                hover_data_dic['index'] = value_index
                hover_data_list.append(hover_data_dic)
                hover_dic['hoverContent'] = hover_content[i]
                hover_dic['hoverData'] = hover_data_list
                hover_list.append(hover_dic)

        return hover_list

