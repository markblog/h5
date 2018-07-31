from .base_chart import BaseChart

class WaterfallChart(BaseChart):
    """
    HeatmapChart is the class of displaying heatmap chart.

    """

    def __init__(self):
        super().__init__()
        self.__type__ = 'waterfall'
        # self.__description__ = 'waterfall chart'

    def _available_types(self):
        self.available_types = ['waterfall']

    def transformation(self, raw_data):
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)
        x_label, y_label = xAxis[0], yAxis[0]
        # self._check_pivot(raw_data, xAxis, yAxis)
        self.__xAxis__ = {
            'type': 'category'
        }

        self.__yAxis__ = {
            'title': {
                'text': df[y_label].iloc[0]
            }
        }

        series = []

        for index, row in df.iterrows():

            if index == 0:
                continue
            else:
                series.append({
                        'name': row[x_label],
                        'y': float(row[y_label])
                    })

        self.__series__ = series
        self.__highlight__ = self._get_hover_data(raw_data, df, x_label)

    def _get_hover_data(self, raw_data, df, x_label, y_count = 0):
        hover_list = []
        highlight, df_highlights = raw_data['df_highlights']
        _, hover_content = raw_data['narrative_highlights'] 

        if highlight:
            for i in range(len(df_highlights)):
                hover_dic = {}
                hover_data_dic = {}
                hover_data_list = [] 

                index = 0
                for y_name in self.__series__:
                    if y_name.get('name') == hover_content[i]:
                        break
                    index += 1


                hover_data_dic['group'] = 0
                hover_data_dic['index'] = index
                hover_data_list.append(hover_data_dic)
                hover_dic['hoverContent'] = hover_content[i]
                hover_dic['hoverData'] = hover_data_list
                hover_list.append(hover_dic)

        return hover_list

    def _check_pivot(self, raw_data, xAxis, yAxis):
        df = raw_data['data']
        # print(df)
        if raw_data.get('pivot'):
            df.drop(df.index[0])
            print('drop')
            print(df) 


