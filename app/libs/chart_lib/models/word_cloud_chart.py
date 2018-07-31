from .base_chart import BaseChart

class WordcloudChart(BaseChart):
    """
    WordcloudChart is the class of exposing the chart in cloud shape.

    """


    def __init__(self):
        super().__init__()
        self.__type__ = 'wordcloud'
        self.__description__ = 'wordcloud chart'
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['wordcloud','line', 'column', 'bar', 'table']

    def transformation(self, raw_data):
        print('wordcloud')
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)

        dic = {}
        dic['name'] = df[yAxis[0]][0]
        weights = self._normalize_weight(df[yAxis[0]][1:])
        dic['data'] = []
        for name, value, weight in zip(df[xAxis[0]][1:], df[yAxis[0]][1:], weights):
            dic['data'].append({'name': name, 'value': float(value), 'weight': weight, 'metric':df[yAxis[0]][0]})

        self.__series__.append(dic)