import pandas as pd
import numpy as np
import math
import os
from collections import OrderedDict
import glob

class narrative_point:
    
    def __init__(self):
    
        #temp = df_for_general[df_for_general['Filename'] == file_df['chart'].tolist()[0]]    
        #self.ctype = temp[temp['Tag_Type'] == 'Type']['Tag_Name'].values[0]
        pass
        
    def SLOPESTD(self, pieces):
        st = pieces[0][0]
        et = pieces[0][1]
        Y_name = pieces[0][2]
        Y_flag = pieces[0][3]
        Y_mag = pieces[0][4]
        narrative_dict = {'SLOPESTD':{}}
        first_sentence = 'From {} to {}, {} {} {}'.format(st, et, Y_name, Y_flag, Y_mag)
        
        if len(pieces) > 1:
            std_flag = pieces[1][-1]
            second_sentence = 'with {}'.format(std_flag)
            sentence = first_sentence + ',' + second_sentence
            narrative_dict['SLOPESTD']['narrative'] = sentence
            
        else:
            sentence = first_sentence
            narrative_dict['SLOPESTD']['narrative'] = sentence
            
        narrative_dict['SLOPESTD']['score'] = 0 #currently we don't want to highlight slope
        narrative_dict['SLOPESTD']['narrative_highlights'] = []
        narrative_dict['SLOPESTD']['df_highlights'] = []
        
        return narrative_dict
    
    def CORR(self, pieces):
        #Only return negative
        #[Y1_name, Y2_name, value, score, display_x, flag]
        if len(pieces) == 0:
            return None
        
        else:
            narrative_dict = {'CORR':{}}
            Y1_name = pieces[0]
            Y2_name = pieces[1]
            display_x = pieces[-2]
            flag = pieces[-1]
            sentence = 'Generally speaking, the correlation between {} and {} in {} is {}'
            sentence = sentence.format(Y1_name, Y2_name, display_x, flag)
            narrative_dict['CORR']['narrative'] = sentence
            narrative_dict['CORR']['score'] = 0 #we currently don't want to highlight CORR
            narrative_dict['CORR']['narrative_highlights'] = [Y1_name, Y2_name]
            narrative_dict['CORR']['df_highlights'] = [Y1_name, Y2_name]
            
            return narrative_dict
      
    
    def SMO(self, pieces):
           
        if pieces[0] < 5:
            
            return None
        
        elif len(pieces[-2]) + len(pieces[-3]) < 2:
            
            return None
        
        else:
            
            narrative_dict = {'SMO':{}}
            X_name_list = pieces[1]
            X_name = ','.join([x.split('_')[-1] for x in X_name_list])
            Y_name_list_neg = pieces[-2]
            Y_name_list_pos = pieces[-3]
            Y_name_neg = ','.join(Y_name_list_neg)
            Y_name_pos = ','.join(Y_name_list_pos)
            narrative_dict['SMO']['score'] = pieces[0]
            narrative_dict['SMO']['narrative_highlights'] = [X_name]
            narrative_dict['SMO']['df_highlights'] = X_name_list
            
            if (pieces[-1] == 'same') & (len(pieces[-2]) > 0):
                
                sentence = 'In {}, {} are simultaneously small'.format(X_name, Y_name_neg)
                narrative_dict['SMO']['narrative'] = sentence
                return narrative_dict
            
            elif (pieces[-1] == 'same') & (len(pieces[-3]) > 0):
                
                sentence = 'In {}, {} are simultaneously large'.format(X_name, Y_name_pos)
                narrative_dict['SMO']['narrative'] = sentence
                return narrative_dict
            
            elif pieces[-1] == 'opp':
                
                sentence = 'In {}, while {} to be large, {} is rather small'.format(X_name, Y_name_pos, Y_name_neg)
                narrative_dict['SMO']['narrative'] = sentence
                return narrative_dict
                

    
    def MAXMIN(self, pieces):
        #[X_name, Y_name, value, score, chart_type, max_or_min]
        if len(pieces) == 0:
            return None

        else:
            narrative_dict = {'MAXMIN':{}}
            X_name_list = pieces[0][0]
            X_name = ','.join([x.split('_')[-1] for x in X_name_list])
            Y_name = pieces[0][1]
            desc = pieces[0][-1]
            value_max = int(pieces[0][2])
            chart_type = pieces[0][4]

            if chart_type in ['LINE', 'MUTIPLE-LINE']:
                if desc == 'largest':
                    sentence = '{} reaches the peak at {} to {}'.format(Y_name, X_name, value_max)
                elif desc == 'lowest':
                    sentence = '{} hits the bottom at {} to {}'.format(Y_name, X_name, value_max)
            else:
                first_sentence = '{} has the {} {} of {}'
                sentence = first_sentence.format(X_name, desc, Y_name, value_max)

            narrative_dict['MAXMIN']['score'] = pieces[0][3]
            narrative_dict['MAXMIN']['narrative_highlights'] = [X_name]
            narrative_dict['MAXMIN']['df_highlights'] = X_name_list

            if len(pieces) < 2:

                narrative_dict['MAXMIN']['narrative'] = sentence
                return narrative_dict

            else:
                X_name_list = pieces[1][0]
                X_name = ','.join([x.split('_')[-1] for x in X_name_list])
                Y_name = pieces[1][1]
                desc = pieces[1][-1]
                value_min = int(pieces[1][2])
                value_range = np.abs(value_max - value_min)

                if chart_type in ['LINE', 'MUTIPLE-LINE']:
                    if desc == 'largest':
                        second_sentence = 'while the value reaches the peak at {} to {}, with range {}'.format(X_name, value_min, value_range)
                    elif desc == 'lowest':
                        second_sentence = 'while the value hits the bottom at {} to {}, with range {}'.format(X_name, value_min, value_range)
                else:
                    second_sentence = 'while {} has the {} of {}, with the range {}'
                    second_sentence = second_sentence.format(X_name, desc, value_min, value_range)

                sentence = sentence + ',' + second_sentence
                narrative_dict['MAXMIN']['narrative'] = sentence
                return narrative_dict


        
        
    def Interval(self, pieces):
        #[Mono_flag, Y, st, et, sv, ev, score]
        narrative_dict = {'MONO INTERVAL':{}}
        if pieces[-1] < 5:
            return None
        else:
            sv,ev = pieces[4], pieces[5]
            if sv < ev:
                increase_flag = 'increase'
            else:
                increase_flag = 'decrease'

            Y_name = pieces[1]
            st = pieces[2]
            et = pieces[3]
            st_short = st.split('_')[1]
            et_short = et.split('_')[1]
            
            sentence = 'The most significant {} happens between {} and {}, {} from {} to {}'.format(increase_flag, st_short, et_short, Y_name, sv, ev)
            narrative_dict['MONO INTERVAL']['score'] = pieces[-1]
            narrative_dict['MONO INTERVAL']['df_highlights'] = [st, et]
            narrative_dict['MONO INTERVAL']['narrative_highlights'] = [st_short, et_short]
            narrative_dict['MONO INTERVAL']['narrative'] = sentence
            
            return narrative_dict
        
        
    
    def Top(self, pieces):
        #Y_name, X_pos, pos_percent, X_neg, neg_percent, flag, ratio, num, Y_name_top
        if len(pieces) == 0:
            return None
        else:
            narrative_dict = {'TOP':{}}
            ratio = pieces[-3]
            num = pieces[-2]
            if ratio < 0.68 or num < 2:
                return None
            else:
                narrative_dict['TOP']['score'] = int(ratio * 10)
                ratio = "{0:.0f}%".format(ratio * 100)
                Y_name = pieces[0]
                Y_name_top = pieces[-1]


                if pieces[-4] == 'top':
                    X_name = ','.join([x[-1].split('_')[-1] for x in pieces[1]])
                    X_name_list = [x[0] for x in pieces[1]]
                    sentence = 'The top {} {} makes up {} of {}, which are {}'.format(num, Y_name, ratio, Y_name_top,X_name)
                    narrative_dict['TOP']['narrative_highlights'] = [X_name]
                    narrative_dict['TOP']['df_highlights'] = X_name_list
                    narrative_dict['TOP']['narrative'] = sentence

                if pieces[-4] == 'bottom':
                    X_name = ','.join([x[-1].split('_')[-1] for x in pieces[3]])
                    X_name_list = [x[0] for x in pieces[3]]
                    sentence = 'The bottom {} {} makes up {} of {}, which are {}'.format(num, Y_name, ratio, Y_name_top,X_name)
                    narrative_dict['TOP']['narrative_highlights'] = [X_name]
                    narrative_dict['TOP']['df_highlights'] = X_name_list
                    narrative_dict['TOP']['narrative'] = sentence

                return narrative_dict


class extract_points:

    def __init__(self, measure_df, datafile, tagfile):
        
        self.measure_df = measure_df
        self.datafile = datafile
        self.tagfile = tagfile
        
    def maxmin_points(self, index):
        
        index_meausre_df = self.measure_df[self.measure_df['NUM'] == index]
        X_name = index_meausre_df[index_meausre_df['submeasure'] == 'X']['content'].values[0]
        Y_name = index_meausre_df[index_meausre_df['submeasure'] == 'Y']['content'].values[0]
        value = index_meausre_df[index_meausre_df['submeasure'] == 'value']['content'].values[0]
        score = index_meausre_df[index_meausre_df['submeasure'] == 'score']['content'].values[0]
        chart_type = self.tagfile['Type'].values[0]
        
        return [X_name, Y_name, value, score, chart_type]
    
    def correlation_points(self, index):
        
        index_meausre_df = self.measure_df[self.measure_df['NUM'] == index]
        Y1_name = index_meausre_df[index_meausre_df['submeasure'] == 'Y1']['content'].values[0]
        Y2_name = index_meausre_df[index_meausre_df['submeasure'] == 'Y2']['content'].values[0]
        value = index_meausre_df[index_meausre_df['submeasure'] == 'value']['content'].values[0]
        score = index_meausre_df[index_meausre_df['submeasure'] == 'score']['content'].values[0]
        display_x_col = [x for x in self.tagfile.columns if x.startswith('X')][-1]
        display_x_name = self.tagfile[display_x_col].values[0]
        
        return [Y1_name, Y2_name, value, score, display_x_name]
    
    def slope_points(self, index):
        
        index_meausre_df = self.measure_df[self.measure_df['NUM'] == index]
        st = index_meausre_df[index_meausre_df['submeasure'] == 'START_TIME']['content'].values[0]
        et = index_meausre_df[index_meausre_df['submeasure'] == 'END_TIME']['content'].values[0]
        Y = index_meausre_df[index_meausre_df['submeasure'] == 'Y']['content'].values[0]
        value = index_meausre_df[index_meausre_df['submeasure'] == 'value']['content'].values[0]
        score = index_meausre_df[index_meausre_df['submeasure'] == 'score']['content'].values[0]
        
        return [st, et, Y, value, score]
    
    def std_points(self, index):
        
        index_meausre_df = self.measure_df[self.measure_df['NUM'] == index]
        Y_name = index_meausre_df[index_meausre_df['submeasure'] == 'Y']['content'].values[0] 
        score = index_meausre_df[index_meausre_df['submeasure'] == 'score']['content'].values[0] 
        
        return [Y_name, score]

    def interval_points(self, index, submeasure):
        
        index_meausre_df = self.measure_df[self.measure_df['NUM'] == index]
        Mono_flag = index_meausre_df[index_meausre_df['submeasure'] == 'Y']['content'].values[0]
        dr = index_meausre_df[index_meausre_df['submeasure'] == submeasure + '_interval']['content'].values[0]
        vr = index_meausre_df[index_meausre_df['submeasure'] == submeasure + '_interval_amount']['content'].values[0]
        score = index_meausre_df[index_meausre_df['submeasure'] == submeasure + '_interval_score']['content'].values[0]
        
        Y = index_meausre_df[index_meausre_df['submeasure'] == 'Y']['content'].values[0]
        
        #st, et = dr[0][0].split('_')[1],  dr[1][0].split('_')[1]
        st, et = dr[0][0],  dr[1][0]
        sv, ev = vr[0], vr[1]
        
        return [Mono_flag, Y, st, et, sv, ev, score]
        
    
    def smo_points(self):
        
        score = self.measure_df[self.measure_df['submeasure'] == 'score']['content'].values[0]
        X_name = self.measure_df[self.measure_df['submeasure'] == 'X']['content'].values[0]
        Y_posname = self.measure_df[self.measure_df['submeasure'] == 'Y_pos']['content'].values[0]
        Y_negname = self.measure_df[self.measure_df['submeasure'] == 'Y_neg']['content'].values[0]
        
        return [score, X_name, Y_posname, Y_negname]
    
    def top_points(self, index):
        
        index_meausre_df = self.measure_df[self.measure_df['NUM'] == index]
        Y_name = index_meausre_df[index_meausre_df['submeasure'] == 'Y']['content'].values[0]
        X_pos = index_meausre_df[index_meausre_df['submeasure'] == 'X_pos']['content'].values[0]
        pos_percent = index_meausre_df[index_meausre_df['submeasure'] == 'pos_percent']['content'].values[0]
        X_neg = index_meausre_df[index_meausre_df['submeasure'] == 'X_neg']['content'].values[0]
        neg_percent = index_meausre_df[index_meausre_df['submeasure'] == 'neg_percent']['content'].values[0]
        
        return [Y_name, X_pos, pos_percent, X_neg, neg_percent]
    
class extract_methods:
    
    def __init__(self, file_df, datafile, tagfile):
        self.npi = narrative_point_identifier(file_df)
        self.datafile = datafile
        self.tagfile = tagfile
    
    def extract_maxmin(self):
        #EXTRACT ENTITY WITH LARGETST SCORE
        dmax = self.npi.get_scores('MAX')
        dmin = self.npi.get_scores('MIN')
        maxmaxkey = max(dmax, key = dmax.get)
        maxminkey = max(dmin, key = dmin.get)
        
        if dmax[maxmaxkey] > dmin[maxminkey]:
            max_or_min = 'largest'
            temp = self.npi.get_file_measure('MAX')
            maxmin_list = extract_points(temp,self.datafile, self.tagfile).maxmin_points(maxmaxkey)
            maxmin_list.append('largest')
            while_list = extract_points(self.npi.get_file_measure('MIN'), self.datafile, self.tagfile).maxmin_points(maxmaxkey)
            while_list.append('lowest')
        
        else:
            max_or_min = 'lowest'
            temp = self.npi.get_file_measure('MIN')
            maxmin_list = extract_points(temp,self.datafile, self.tagfile).maxmin_points(maxminkey)
            maxmin_list.append('lowest')
            while_list = extract_points(self.npi.get_file_measure('MAX'), self.datafile, self.tagfile).maxmin_points(maxminkey)
            while_list.append('largest')

        #Rule out max/min value in a line chart happens in the first
        #print(self.tagfile['Type'].values[0])
        if self.tagfile['Type'].values[0] == 'LINE':
            #print(maxmin_list[0][0], self.datafile['X1'][1])
            if maxmin_list[0][0].split('_')[1] == self.datafile['X1'][1] or while_list[0] == self.datafile['X1'][1]:
                return []
            else:
                pass
        
        if while_list[3] > 5:
            return [maxmin_list, while_list]
        
        else:
            return [maxmin_list]
            
    
    def extract_corr(self):
        #EXTRACT ENTITY WITH LARGETST SCORE
        dcorr = self.npi.get_scores('CORR')
        temp = self.npi.get_file_measure('CORR')
        maxcorrkey = max(dcorr, key = dcorr.get)
        mincorrkey = min(dcorr, key = dcorr.get)
        if dcorr[maxcorrkey] >= 7:
            flag = 'negative'
            corr_list = extract_points(temp, self.datafile, self.tagfile).correlation_points(maxcorrkey)
            corr_list.append(flag)
        
        elif dcorr[mincorrkey] <= 3:
            flag = 'positive'
            corr_list = extract_points(temp, self.datafile, self.tagfile).correlation_points(mincorrkey)
            corr_list.append(flag)
            
        else:
            
            corr_list = []
            
        return corr_list
    
    def extract_interval(self):
        #EXTRACT ENTITY WITH LARGETST SCORE
        dinterval = self.npi.get_scores_interval()
        temp = self.npi.get_file_measure('Interval')
        maxintervalkey = max(dinterval, key = dinterval.get)
        num_id = maxintervalkey.split('#')[0]
        submeasure = '_'.join(maxintervalkey.split('#')[1].split('_')[0:2])
        interval_list = extract_points(temp, self.datafile, self.tagfile).interval_points(int(num_id), submeasure)
        
        return interval_list #[Mono_flag, Y, st, et, sv, ev, score]
        
        
    
    def extract_slopestd(self):
        #EXTRACT ENTITY WITH LARGETST SCORE
        dslope = self.npi.get_scores('SLOPE')
        maxslopekey =  max(dslope, key = dslope.get)
        #get slope list
        slope_df = self.npi.get_file_measure('SLOPE')
        slope_list = extract_points(slope_df, self.datafile, self.tagfile).slope_points(maxslopekey)
        if slope_list[-2] > 0: #positive slope
            slope_list[-2] = 'rises'
        else:
            slope_list[-2] = 'drops'
            
        if slope_list[-1] > 5: #large rise - large score
            slope_list[-1] = 'sharply'
        else:
            slope_list[-1] = 'mildly'
        
        #get std list
        std_df = self.npi.get_file_measure('STD')
        std_list = extract_points(slope_df, self.datafile, self.tagfile).std_points(maxslopekey)
        std_score = std_list[-1]
        if std_score > 6:
            std_flag  = 'large fluctuation'
            std_list.append(std_flag)
            return [slope_list, std_list]
            
        elif std_score < 4:
            std_flag  = 'small fluctuation'
            std_list.append(std_flag)
            return [slope_list, std_list]
        
        else:
            return [slope_list]
    
    def extract_smo(self):
        
        smo_df = self.npi.get_file_measure('SMO')
        smo_list = extract_points(smo_df, self.datafile, self.tagfile).smo_points()
        if len(smo_list[-1]) > 0 & len(smo_list[-2]) > 0:
            smo_flag = 'opp'
        else:
            smo_flag = 'same'
        smo_list.append(smo_flag)
        
        return smo_list #[score, X_name, Y_posname, Y_negname, smo_flag]
    
    def extract_top(self):

        top_dict = {'EMV':'holdings', 'BMV':'holdings', 'MANAGE EXPENSES':'expenses','PERIOD VALUE ADD':'value add',
                   'NET CASH FLOWS': 'flows'}
        top_df = self.npi.get_file_measure('Top')
        dtop = self.npi.get_scores_top()
        if len(dtop) == 0:
            return []
        else:
            maxtopkey = max(dtop, key = dtop.get).split('#')[0]
            top_list = extract_points(top_df, self.datafile, self.tagfile).top_points(int(maxtopkey))
            pos_percent, neg_percent = top_list[2], top_list[-1]
            if pos_percent > neg_percent:
                flag = 'top'
                ratio = pos_percent
                num = len(top_list[1])
            elif pos_percent < neg_percent:
                flag = 'bottom'
                ratio = neg_percent
                num = len(top_list[3])
            else:
                flag = 'none'
                ratio = 0
                num = 0
            Y_name = top_list[0]
            Y_name_top = top_dict[Y_name]

            if Y_name == 'PERIOD VALUE ADD' or Y_name == 'NET CASH FLOWS':
                if flag == 'top':
                    Y_name_top = 'positive '+ Y_name_top
                elif flag == 'bottom':
                    Y_name_top = 'negative '+ Y_name_top


            top_list.append(flag)
            top_list.append(ratio)
            top_list.append(num)
            top_list.append(Y_name_top)

            return top_list #Y_name, X_pos, pos_percent, X_neg, neg_percent, flag, ratio, num, Y_name_top


class narrative_point_identifier():
    
    
    def __init__(self, file_df):
        
        self.narrative_point = file_df.fillna(0)
    
    def get_measure(self):
        
        return set(self.narrative_point['measure'])
    
    def get_file_measure(self, measure):
        
        return self.narrative_point[self.narrative_point['measure'] == measure]
    
    def get_scores(self, measure):
        
        numtoscore = {}
        file_df_measure = self.narrative_point[self.narrative_point['measure'] == measure]
        file_df_measure_score = file_df_measure[file_df_measure['submeasure'] == 'score']
        
        for i in range(0, file_df_measure_score.shape[0]):
            
            k,v = file_df_measure_score.iloc[i]['NUM'], file_df_measure_score.iloc[i]['content']
            numtoscore[k] = v
            
        return numtoscore
    
    def get_scores_interval(self):
        
        numsubtoscore = {}
        file_df_measure = self.narrative_point[self.narrative_point['measure'] == 'Interval']
        num_y = set(self.narrative_point['NUM'])
        submeasures = ['highest_increase_interval_score', 'highest_decrease_interval_score',
                      'longest_increase_interval_score','longest_decrease_interval_score']
        for y_id in num_y:
            for m_id in submeasures:
                key = str(y_id) + '#' + m_id
                
                value = file_df_measure[(file_df_measure['submeasure'] == m_id) & (file_df_measure['NUM'] == y_id)]['content']
                #set_trace()
                numsubtoscore[key] = value.values[0]
        
        return numsubtoscore
    
    def get_scores_top(self):
        
        top_y_list = ['EMV','BMV','MANAGE EXPENSES','PERIOD VALUE ADD','NET CASH FLOWS']
        numsubtoscore = {}
        file_df_measure = self.narrative_point[self.narrative_point['measure'] == 'Top']
        num_y = set(file_df_measure['NUM'])
        
        #condition = file_df_measure[(file_df_measure['NUM'] == y) & (file_df_measure['submeasure'] == 'Y')]['content'].values[0] in top_y_list
        filtered_num_y = [y for y in num_y if file_df_measure[(file_df_measure['NUM'] == y) & (file_df_measure['submeasure'] == 'Y')]['content'].values[0] in top_y_list]
        submeasures = ['pos_percent', 'neg_percent']
        #print(filtered_num_y)
        for y_id in filtered_num_y:
            for m_id in submeasures:
                key = str(y_id) + '#' + m_id
                value = file_df_measure[(file_df_measure['submeasure'] == m_id) & (file_df_measure['NUM'] == y_id)]['content']
                #set_trace()
                numsubtoscore[key] = value.values[0]
        
        return numsubtoscore


class get_file_narratives:
    
    def __init__(self, df_for_narr, prdatafile_list, prtagfile_list, filename):
        
        self.prdatafile_list = prdatafile_list
        self.df = self.prdatafile_list[filename]
        
        self.prtagfile_list = prtagfile_list
        self.tf = self.prtagfile_list[filename]
        
        self.df_for_narr = df_for_narr
        
        self.narr_dict = OrderedDict()
        file_df = self.df_for_narr[self.df_for_narr['chart'] == filename]
        name = file_df['chart'].tolist()[0]
        em = extract_methods(file_df, self.df, self.tf)
        narrative_measures = self.prtagfile_list[filename]['Narrative_element'].values[0].split(',')
        
        for nm in narrative_measures:
           
            measure_dict = self.narrative_measrue(nm, em)
            if measure_dict != None:
                k,v  = list(measure_dict.keys())[0], list(measure_dict.values())[0]
                self.narr_dict[k] = v
        
        
    def narrative_measrue(self, measure, em):
        if measure == 'MAXMIN':

            return narrative_point().MAXMIN(em.extract_maxmin())

        if measure == 'CORR':

            return narrative_point().CORR(em.extract_corr())

        if measure == 'SLOPESTD':

            return narrative_point().SLOPESTD(em.extract_slopestd())

        if measure == 'MONO INTERVAL':

            return narrative_point().Interval(em.extract_interval())

        if measure == 'SUM OUT':

            return narrative_point().SMO(em.extract_smo())

        if measure == 'TOP':

            return narrative_point().Top(em.extract_top())

    def get_narrative(self):

        narr_keys = list(self.narr_dict.keys())
        while len(narr_keys) > 3:
            for key in [i for i in ['MAXMIN','TOP'] if i in narr_keys]:
                narr_keys.remove(key)

        narr_list = []
        for narr_key in narr_keys:
            narr_list.append(self.narr_dict[narr_key]['narrative'])

        final_narrative = '.'.join(narr_list)
        
        return final_narrative
    
    def get_highlight(self):
        
        max_key = max(self.narr_dict, key = lambda x: self.narr_dict[x]['score'])
        
        return self.narr_dict[max_key]['df_highlights'], self.narr_dict[max_key]['narrative_highlights']
        
        
        
    