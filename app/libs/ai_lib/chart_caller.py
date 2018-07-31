"""

Input: 
     
     corr_method: 'jac' or 'cosine' 
     alpha: parameter for pagerank
     score_dict_path: path for score dictionary
     interest_point_table_path: path for the interest point table
     prdatafile_path: paths for all pagerank datafiles
     prtagfile_path: paths for all pagerank tagfiles
     
Main methods: 
     
     get_first_k_charts: return a Orderdict of first k charts in our filtered chart list 
     get_charts_by_page: return charts in a Orderdict in a given page with number of charts per page provided
     get_charts_details: given a filename, return detailed chart dictionary
     get_related_charts: given a filename and a number return a Ordereddict of related charts


"""
import glob
from collections import defaultdict, OrderedDict
import os
import pandas as pd
import pickle

#########NEXT SECTION IS ABOUT OWM MODULE
from .charts_provider import charts_provider
from .chart_extractor import chart_extractor
from .picture_plot_dict import picture_plot_dict
from .chart_narrative import chart_narrative
from .chart_alert import chart_alert

class acquire_charts():
    
    def __init__(self, method, alpha, score_dict_path, prdatafile_path, prtagfile_path, interest_point_table_path, thresh_dict_path, percentile_dict_path):
        
        self.prdatafile_path = prdatafile_path
        self.prtagfile_path = prtagfile_path
        self.allprdatafile = glob.glob(os.path.join(self.prdatafile_path, "**", "*.csv"), recursive=True)
        self.allprtagfile = glob.glob(os.path.join(self.prtagfile_path, "**", "*.csv"), recursive=True)

        self.prtagfile_list = OrderedDict()
        for x in self.allprtagfile:
            self.prtagfile_list[x.split("\\")[-1].split('.')[0]] = pd.read_csv(x)
        
        self.prdatafile_list = OrderedDict()
        for x in self.allprdatafile:
            self.prdatafile_list[x.split("\\")[-1].split('.')[0]] = pd.read_csv(x)

        self.all_plot_dict = {}
        self.cp = charts_provider(method, alpha, score_dict_path, prdatafile_path, prtagfile_path, interest_point_table_path)
        self.all_chart_shown = self.cp.first_x_chart()
        
        chart_ext = chart_extractor(self.prdatafile_list, self.prtagfile_list)
        chart_ext.get_plot_df()
        self.Allfilename = chart_ext.All_filename
        self.picinfodf = chart_ext.picture_info_df
        self.pic_type_df = defaultdict(dict)
        self.narrative_highlight_dict = None
        self.alert_dict = None
        self.thresh_dict_path = thresh_dict_path
        self.percentile_dict_path = percentile_dict_path


    def get_narrative_dict(self):
        cn = chart_narrative(self.prdatafile_list, self.prtagfile_list, self.percentile_dict_path)

        self.narrative_highlight_dict = cn.get_all_narrative_and_highlights()

    def get_alert_dict(self):

        ca = chart_alert(self.thresh_dict_path, self.prdatafile_list, self.prtagfile_list)
        self.alert_dict = ca.get_alert_bool_narrative()

    def get_all_plot_dict(self):
        print('Generating Narratives...')
        self.get_narrative_dict()
        print('Done')

        print('Generating Alerts...')
        self.get_alert_dict()
        print('Done')

        for i, filename in enumerate(self.Allfilename):

            df = self.prdatafile_list[filename]
            tf = self.prtagfile_list[filename]
            file = picture_plot_dict(filename, df, tf, self.picinfodf)
            file.generate_picture_plot_dict()
            self.all_plot_dict[filename] = file.picture_plot_dict
            res1, res2 = self.cp.recommend_chart(filename)
            all_related_charts = res1+res2

            self.all_plot_dict[filename]['related_charts'] = all_related_charts
            self.all_plot_dict[filename]['summary'] = self.narrative_highlight_dict[filename]['narrative']
            self.all_plot_dict[filename]['df_highlights'] = self.narrative_highlight_dict[filename]['df_highlights']
            self.all_plot_dict[filename]['narrative_highlights'] = self.narrative_highlight_dict[filename]['narrative_highlights']
            self.all_plot_dict[filename]['alert'] = (self.alert_dict[filename]['BOOL'], self.alert_dict[filename]['NARRATIVE'])


            chart_type = self.all_plot_dict[filename]['type']
            self.pic_type_df[chart_type]['data'] = self.all_plot_dict[filename]['data']
            self.pic_type_df[chart_type]['title'] = self.all_plot_dict[filename]['title']
            self.pic_type_df[chart_type]['id'] = filename
    
    def get_first_k_charts(self, k):
        
        if len(self.all_chart_shown) < k: 
            
            print('The number of charts required excesses the number of charts provided')
        
        first_k_chart = OrderedDict()
        for c in self.all_chart_shown[0:k]:
            
            first_k_chart[c] = self.all_plot_dict[c]
        
        return first_k_chart
    
    def get_charts_by_page(self, page_no, page_size = 6, level = 'manager'):
        """
        params:
            page_no:  page number of the charts
            page_size: the number of the charts would give to front end
        return:
            Ordedict {key:Filename, value: chart detail dict}
        """
        if level.lower() == 'manager':
            chart_details = OrderedDict()
            chart_index_start = (page_no - 1) * page_size
            chart_index_end = page_no * page_size
            len_all_chart = len(self.all_chart_shown)

            if chart_index_start > len_all_chart:

                print('The number of charts required excesses the number of charts provided')

            if chart_index_end > len_all_chart:

                chart_index_end = len_all_chart

            for i in range(chart_index_start, chart_index_end):
                chart_details[self.all_chart_shown[i]] = self.all_plot_dict[self.all_chart_shown[i]]

            return chart_details, chart_index_end >= len_all_chart, len_all_chart

        else:
            return {}, True, len_all_chart
    
    def get_charts_details(self, filename):
        
        return self.all_plot_dict[filename]
    
    
    def get_related_charts(self, filename, k):
        
        """
        params:
            filename: chart name
            k: number of related charts extracted
        return:
            Ordedict {key:Filename, value: chart detail dict}
        """
        related_charts_dict = OrderedDict()
        all_related_charts = self.all_plot_dict[filename]['related_charts']
        for i in all_related_charts[0:k]:
            related_charts_dict[i] = self.all_plot_dict[i]
            
        return related_charts_dict   
        
    def get_pic_type_df(self):
        
        return self.pic_type_df

    def get_alert_id(self):
        """
        return a list of picture id that have alerts.

        """
        alert_id = []
        for k in self.alert_dict:
            if self.alert_dict[k]['BOOL'] is True:

                alert_id.append(k)

        return alert_id

    def get_similar_alert(self, filename, n):

        all_related_charts = self.all_plot_dict[filename]['related_charts']
        alert_chart_ids = self.alert_dict.keys()

        related_alerts = [chart for chart in all_related_charts if chart in alert_chart_ids]
        return related_alerts[:n]