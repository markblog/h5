__author__ = 'V631932'
import glob
import os
from collections import OrderedDict
import pandas as pd


"""
Input:
     prdatafile_path: paths for all pagerank datafiles
     prtagfile_path: paths for all pagerank tagfiles

Main methods:

"""

class chart_extractor():

    def __init__(self, prdatafile_list, prtagfile_list):

        self.prdatafile_list = prdatafile_list
        self.prtagfile_list = prtagfile_list
        self.picture_info_df = None
        self.allprdatafile = None
        self.allprtagfile = None
        self.All_filename = None

    def get_plot_df(self):

        #self.allprdatafile = glob.glob(os.path.join(self.prdatafile_path, "**", "*.csv"), recursive=True)
        #self.allprtagfile = glob.glob(os.path.join(self.prtagfile_path, "**", "*.csv"), recursive=True)

        picture_info_dict = OrderedDict([('Filename',[]), ('Pic_ID',[]), ('Tag_Type',[]), ('Tag_Name',[]), ('Tag_Content',[]) ])
        self.All_filename = []
        for df, tf, filenames in zip(self.prdatafile_list.values(), self.prtagfile_list.values(), self.prdatafile_list.keys()):
            
            Filename = filenames
            self.All_filename.append(Filename)

            Filtercolname = [x for x in tf.columns if x.startswith('Filter')]
            Filtername = [tf.loc[0, x] for x in Filtercolname]

            Typecolname = [x for x in tf.columns if x.startswith('Type')]
            Typename = [tf.loc[0, x] for x in Typecolname]

            #Ygroupcolname = [x for x in tf.columns if x.startswith('Type')]
            #Ygroupname = [tf.loc[0, x] for x in Typecolname]

            Xcolname = [x for x in df.columns if x.startswith('X')]
            Xname = [df.loc[0, x] for x in Xcolname]

            Ycolname = [x for x in df.columns if x.startswith('Y')]
            Yname = [df.loc[0, x] for x in Ycolname]

            pic_id = str(tf.loc[0,'Pic_ID'])
            for f in range(len(Filtername)):

                picture_info_dict['Filename'].append(Filename)
                picture_info_dict['Tag_Type'].append(Filtercolname[f])
                picture_info_dict['Tag_Name'].append(Filtername[f])
                #temp = list(set(tf.loc[1:,Filtercolname[f]]))
                temp = list(OrderedDict.fromkeys(tf.loc[1:,Filtercolname[f]]))
                cleandtemp = [x for x in temp if str(x) != 'nan']
                picture_info_dict['Tag_Content'].append(cleandtemp)
                picture_info_dict['Pic_ID'].append(pic_id)

            for x in range(len(Xname)):

                picture_info_dict['Filename'].append(Filename)
                picture_info_dict['Tag_Type'].append(Xcolname[x])
                picture_info_dict['Tag_Name'].append(Xname[x])
                #temp = list(set(df.loc[1:,Xcolname[x]]))
                temp = list(OrderedDict.fromkeys(tf.loc[1:,Xcolname[x]]))
                cleandtemp = [x for x in temp if str(x) != 'nan']
                picture_info_dict['Tag_Content'].append(cleandtemp)
                picture_info_dict['Pic_ID'].append(pic_id)

            for y in range(len(Yname)):

                picture_info_dict['Filename'].append(Filename)
                picture_info_dict['Tag_Type'].append(Ycolname[y])
                picture_info_dict['Tag_Name'].append(Yname[y])
                #temp = list(set(df.loc[1:,Ycolname[y]]))
                temp = list(OrderedDict.fromkeys(tf.loc[1:,Ycolname[y]]))
                cleandtemp = [x for x in temp if str(x) != 'nan']
                picture_info_dict['Tag_Content'].append(cleandtemp)
                picture_info_dict['Pic_ID'].append(pic_id)

            for t in range(len(Typename)):

                picture_info_dict['Filename'].append(Filename)
                picture_info_dict['Tag_Type'].append(Typecolname[t])
                picture_info_dict['Tag_Name'].append(Typename[t])
                temp = list(set(tf.loc[1:,Typecolname[t]]))
                cleandtemp = [x for x in temp if str(x) != 'nan']
                picture_info_dict['Tag_Content'].append(cleandtemp)
                picture_info_dict['Pic_ID'].append(pic_id)

            if 'TOP' in Filename:

                picture_info_dict['Filename'].append(Filename)
                picture_info_dict['Tag_Type'].append('FilterTopkFilter')
                picture_info_dict['Tag_Name'].append('TopkFilter')

                picture_info_dict['Tag_Content'].append([tf['TopkFilter'].values[0]])
                picture_info_dict['Pic_ID'].append(pic_id)

        self.picture_info_df = pd.DataFrame(picture_info_dict)