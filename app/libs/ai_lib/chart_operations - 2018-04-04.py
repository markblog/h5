from collections import OrderedDict
import numpy as np

class Chartoperation:
    
    def __init__(self, chart_dict_all, shown_chart_names, single_entity_dict):
        
        self.chart_dict_all = chart_dict_all
        self.chart_dict_filtered = {x: self.chart_dict_all[x] for x in shown_chart_names}
        self.single_entity_dict = single_entity_dict
        self.shown_chart_names = shown_chart_names

    def get_charts_details(self, filename):
        return self.chart_dict_all[filename]
    
    def get_related_charts(self, filename, k):
        """
        params:
            filename: chart name
            k: number of related charts extracted
        return:
            Ordedict {key:Filename, value: chart detail dict}
        """
        related_charts_dict = OrderedDict()
        all_related_charts = self.chart_dict_all[filename]['related_charts']
        
        for i in all_related_charts[0:k]:
            related_charts_dict[i] = self.chart_dict_all[i]

        return related_charts_dict
    
    def get_first_k_charts(self, k):
        length = len(self.chart_dict_filtered)
        if length < k:
            raise Exception('The number of charts required %s excesses the number of charts provided %s' % (length, k))

        first_k_chart = OrderedDict()
        for c in list(self.chart_dict_filtered.keys())[0:k]:
            first_k_chart[c] = self.chart_dict_filtered[c]
        return first_k_chart
    
    def get_charts_by_page(self, chart_base, page_no, page_size=6, level='manager'):
        """
        params:
            page_no:  page number of the charts
            page_size: the number of the charts would give to front end
            chart_base: a list of chart names to be shown
        return:
            Ordedict {key:Filename, value: chart detail dict}
        """
        if level == 'manager':
            chart_details = OrderedDict()
            chart_index_start = (page_no - 1) * page_size
            chart_index_end = page_no * page_size
            len_all_chart = len(chart_base)
            total_page_num = int(len_all_chart)

            if chart_index_start > len_all_chart:
                raise Exception('The number of charts required excesses the number of charts provided')

            if chart_index_end > len_all_chart:
                chart_index_end = len_all_chart

            for i in range(chart_index_start, chart_index_end):
                chart_details[chart_base[i]] = self.chart_dict_all[chart_base[i]]

            return chart_details, total_page_num
        
        else:
            return {}, 0
    
    def get_singleEntitycharts(self, key_entity):
        
        return self.single_entity_dict[key_entity]