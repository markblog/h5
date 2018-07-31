from .base_chart import BaseChart


class StackedColumnChart(BaseChart):


    def __init__(self):
        super().__init__()
        self.__type__ = 'stacked_column'
        # self.__description__ = 'Stacked column chart'
        self.__xAxis__ = []
        self.__yAxis__ = {
            "title": "rainfall"
        }


    def transformation(self, raw_data):
        # print(raw_data)
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)
        x_label, y_label = xAxis[0], yAxis[0]
        x2_label = xAxis[1]

        if df[x_label][0] == 'DATE RANGE':
            self.__xAxis__ = {'categories': self._date_formatter(df[x_label][1:].values), 'title':x_label}
        else:
            # self.__xAxis__ = {'categories': self._sort_list_preserving_order(df[x_label][1:].values.tolist()), 'title':x_label}
            # print(raw_data.get('pivot')[0], ' -- ', raw_data.get('pivot')[1])
            if raw_data.get('pivot')[0]:
                x = []
                for s in df['X1'][1:].unique():
                    x.append(s)
                self.__xAxis__ = {'categories': x, 'title':x_label}
            else:
                self.__xAxis__ = {'categories': self._sort_list_preserving_order(df[x_label][1:].values.tolist()), 'title':x_label}

        value_column = raw_data.get('pivot')[1]
        x2_list = df[value_column][1:].unique()

        result_list = []
        
        for name in x2_list:
            result_dic ={}
            result = df[(df[value_column] ==name)]['Y1'].tolist()
            result_dic['name'] = name
            if len(result) >= 1:
                result_dic['data'] = [float(r) for r in result]
                result_list.append(result_dic)

        self.__series__ = result_list

        self._get_hover_data(raw_data, df, x_label)

    def _get_hover_data(self, raw_data, df, x_label, y_count = 0):
        hover_list = []
        highlight, df_highlights = raw_data['df_highlights']
        _, hover_content = raw_data['narrative_highlights']

        if highlight:
            for i in range(len(df_highlights)):

                hover_dic = {}
                hover_data_dic = {}
                hover_data_list = [] 

                group_data=df_highlights[i].split("_")[0]
                value_data=df_highlights[i].split("_")[-1]
                # print("*** ",self.__xAxis__["categories"]," ***")
                value_index = -1
                try:
                    if df[x_label][0] == 'DATE RANGE':
                        group_data_index = 0
                        value_index = self.__xAxis__["categories"].index(value_data)
                    else:
                        group_data_index = y_count
                        value_index = self.__xAxis__["categories"].index(value_data)
 
                except Exception as e:
                    pass
                
                if value_index != -1:
                    hover_data_dic['group'] = group_data_index
                    hover_data_dic['index'] = value_index
                    hover_data_list.append(hover_data_dic)
                    hover_dic['hoverContent'] = hover_content[i]
                    hover_dic['hoverData'] = hover_data_list
                    self.__highlight__.append(hover_dic)
