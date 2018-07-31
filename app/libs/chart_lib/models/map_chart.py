import json,os,sys

from .base_chart import BaseChart
from collections import defaultdict


class CountryCode:

    def __init__(self, *args, **kwargs):

        self._load_country_code()

    def _load_country_code(self):

        file_dir = os.path.dirname(__file__)

        with open(os.path.join(file_dir, 'country_code.json')) as f:
            self.country_code_dict = json.load(f)

    def search_country_code(self, country_name):

        for country_code in self.country_code_dict:

            if country_code.get('name').lower().startswith(country_name.lower()):

                return country_code.get('code3')

        return None


country_code = CountryCode()

class MapChart(BaseChart):
    """BarChart is the class of 
    displaying the bar chart information.
    """
    def __init__(self):
        super().__init__()
        self.__type__ = 'map'
        self.__description__ = 'map chart'
        self.__series__ = []

    def _available_types(self):
        self.available_types = ['map']

    def transformation(self, raw_data):
        df = raw_data['data']
        self._set_common_properties(raw_data)
        xAxis, yAxis = self._parse_header(df)
        x_label, y_label = xAxis[0], yAxis[0]

        for index, row in df.iterrows():
            if index == 0:
                continue
            else:
                code3 = country_code.search_country_code(row[x_label])
                if code3:
                    self.__series__.append({
                        'code3': code3,
                        'name': row[x_label],
                        'value': float(row[y_label])
                    })

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