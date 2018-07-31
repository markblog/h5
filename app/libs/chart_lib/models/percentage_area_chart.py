from .base_chart import BaseChart
from collections import defaultdict

class PercentageAreaChart(BaseChart):

    def __init__(self):
        super().__init__()
        self.__type__ = 'percentage_area'
        # self.__description__ = 'percentage_area chart'
        self.__xAxis__ = []
        self.__yAxis__ = {
            "title": "Total percent market share"
        }
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['percentage_area']

    def transformation(self, raw_data):
        self._set_common_properties(raw_data)

        # print(raw_data)
        str = raw_data.get('data')
        groupResult = str.groupby('X2').groups
        result = []
        xAxis = []
        flag = True

        for key,value in groupResult.items():
            name = key
            d = []

            if name == 'PLAN ATTRIBUTION COMPONENT':
                continue
            
            for i in value.values:
                column = str.loc[i]

                d.append(float(column['Y1']))
                if flag:
                    xAxis.append(column['X1'])
            
            result.append({'name':key,'data':d})

            flag = False

        # title = {'text':raw_data.get('F00062_all_0_S2AC').get('title')}
        self.__xAxis__ = xAxis
        self.__series__ = result
        # self._get_hover_data(xAxis)
        self._get_hover_data(xAxis, raw_data)
        # allResult = {
        #     'title': title,
        #     'series':result,
        #     'categories': x
        # }

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

            index = xAxis.index(narrative_highlights[i])
            hover_data_list.append({"group":0, "index":index})

            highlight.append({"hoverData":hover_data_list, "hoverContent":narrative_highlights[i]})
            break;

        self.__highlight__ = highlight

       
        