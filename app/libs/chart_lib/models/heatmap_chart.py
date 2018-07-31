from .base_chart import BaseChart

class HeatmapChart(BaseChart):
    """
    HeatmapChart is the class of displaying heatmap chart.

    """

    def __init__(self):
        super().__init__()
        self.__type__ = 'heatmap'
        # self.__description__ = 'heatmap chart'

    def _available_types(self):
        self.available_types = ['heatmap']

    def transformation(self, raw_data):
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)
        x_label, x2_label, y_label = xAxis[0], xAxis[1], yAxis[0]
        # self._check_pivot(raw_data, xAxis, yAxis)
        x_categories, y_categories = df[x_label].unique().tolist()[1:], df[x2_label].unique().tolist()[1:]

        print(x_categories, y_categories)

        self.__xAxis__ = {
            'categories': x_categories
        }

        self.__yAxis__ = {
            'categories': x_categories
        }

        series = []

        for index, row in df.iterrows():

            if index == 0:
                continue
            else:
                series.append([x_categories.index(row[x_label]), x_categories.index(row[x2_label]), float(row[y_label])])

        self.__series__ = {
            'name': df[y_label].iloc[0],
            'data': series
        }

        self.__highlight__ = self._get_hover_data(raw_data, df, x_label)

    def _get_hover_data(self, raw_data, df, x_label, y_count = 0):
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

    def _check_pivot(self, raw_data, xAxis, yAxis):
        df = raw_data['data']
        print(df)
        if raw_data.get('pivot'):
            df.drop(df.index[0])
            print('drop')
            print(df) 


