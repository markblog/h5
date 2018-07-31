__author__ = 'V631932'
import glob
import os
from collections import defaultdict
from itertools import chain
import numpy as np
import pandas as pd

"""
Input: filepath of datafiles and tagfiles
Output: Charts Feature Matrix by calling method gen_tag_matrix

"""
class get_feature_matrix():

    def __init__(self, prdatafile_path, prtagfile_path):

        self.prdatafile_path = prdatafile_path
        self.prtagfile_path = prtagfile_path
        self.feature_matrix = None
        self.feature_Dict = None
        self.allfiles = glob.glob(os.path.join(prtagfile_path,"**", "*.csv"), recursive=True)
        self.dict_tag_matrix = defaultdict(list)

    def mergedict(self, td1,td2):
        td3 = defaultdict(list)
        for k,v in chain(td1.items(), td2.items()):
            td3[k].extend(v)
            td3[k] = list(set(td3[k]))

        return td3

    def get_col_names(self, tagfile):
        """
        Input a tagfile(DataFrame), return its tags and a tag dictionary
        Except the fileters and axis, tags will also include effective dates and types.
        """
        col_name = []
        Tag_dict = defaultdict(list)
        for i in tagfile.columns:
            if i.startswith('X') or i.startswith('Filter'):

                temp = list(set(tagfile[i][0] + '_' + tagfile[i][1:]))
                temp = [x for x in temp if isinstance(x, str)]
                if tagfile[i][0] == 'EFFECTIVE_DATE':
                    temp = [x.replace('-','')[0:6] for x in DL ]

                col_name.extend(temp)
                Tag_dict[tagfile[i][0]].extend(temp)

            elif i.startswith('Y'):
                temp = tagfile[i][0]
                col_name.append('Y_' + temp)
                Tag_dict['Y'].append('Y_' + temp)


        return col_name, Tag_dict

    def check_df(self, tag_mat):
        """
        Sanity check for tag matrix.
        """
        ind = range(0,tag_mat.shape[0])
        for i in ind:

            the_file = self.allfiles[i]
            col_name,_ = self.get_col_names(pd.read_csv(the_file))

            assert np.sum(tag_mat.loc[i, col_name] == 0) == 0

        print ("Test passed! The feature matrix is what you want.")

    def gen_tag_matrix(self,Tag_dict = {}):
        """
        args: dict_tag_matrix, a tag matrix dict(could be empty), a Tag_dict(could be empty)
        return: A updated sparse tag matrix dict and a updated Tag_dict

        """

        #Tag_dict = {}
        #dict_tag_matrix = defaultdict(list)
        picid_list, classid_list = [], []
        for i,file in enumerate(self.allfiles):
            #print(file)
            tf = pd.read_csv(file)
            picid_list.append(tf['Pic_ID'][0])
            classid_list.append(tf['ClassID'][0])
            col_name,temp_dict = self.get_col_names(tf)
            Tag_dict = self.mergedict(Tag_dict,temp_dict)
            old_keys = list(self.dict_tag_matrix.keys())

            new_keys = [x for x in col_name if x not in old_keys]
            no_exist_keys = [x for x in old_keys if x not in col_name]
            shared_keys = list(set(col_name).intersection(old_keys))

            for ele in new_keys:
                self.dict_tag_matrix[ele] = list(np.zeros(i)) + [1]
            for ele in no_exist_keys:
                self.dict_tag_matrix[ele].append(0)
            for ele in shared_keys:
                self.dict_tag_matrix[ele].append(1)


        self.dict_tag_matrix['Pic_ID'] = picid_list
        self.dict_tag_matrix['ClassID'] = classid_list

        #set_trace()
        self.feature_matrix = pd.DataFrame(self.dict_tag_matrix)
        self.feature_Dict = Tag_dict

        self.check_df(self.feature_matrix)

        prfile_index = [x.split('\\')[-1][0:-4] for x in self.allfiles]

        self.feature_matrix['Filename'] = prfile_index

        for cnames in self.feature_Dict['DATE RANGE']:

            date = cnames.split('_')[1]
            efdate = 'EFFECTIVE DATE_' + date

            self.feature_matrix[efdate] = self.feature_matrix[efdate] + self.feature_matrix[cnames]

        self.feature_matrix = self.feature_matrix.drop(self.feature_Dict['DATE RANGE'], axis = 1)