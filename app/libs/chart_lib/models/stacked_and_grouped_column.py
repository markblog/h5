from .base_chart import BaseChart
from collections import defaultdict

class StackedAndGroupedChart(BaseChart):


    def __init__(self):
        super().__init__()
        self.__type__ = 'column'
        self.__description__ = 'Stacked column chart'
        self.__xAxis__ = []
        self.__yAxis__ = {
            "title": "rainfall"
        }

    def transformation(self, raw_data):
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)
        x_label, y_label = xAxis[0], yAxis[0]

        if df[x_label][0] == 'DATE RANGE':
            self.__xAxis__ = {'categories': sorted(self._date_formatter(df[x_label][1:].values)), 'title':x_label}
        else:
            self.__xAxis__ = {'categories': _sort_list_preserving_order(sorted(df[x_label][1:].values.tolist())), 'title':x_label}

        result_list = []
        x2_list = df['X2'][1:].unique()
        x3_list = df['X3'][1:].unique()

        for name in x2_list:
            for stack in x3_list:
                result_dic ={}
                result = df[(df['X2'] ==name)& (df['X3'] ==stack)]['Y1'].tolist()
                result_dic['name'] = name
                result_dic['stack'] = stack
                if len(result) >= 1:
                    result_dic['data'] = result
                    result_list.append(result_dic)        
        self.__series__.append(result_list)

