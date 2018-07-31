__author__ = 'V631932'
import pickle
import pandas as pd
from collections import defaultdict
import numpy as np
#from sklearn.metrics.pairwise import cosine_similarity,pairwise_distances
import time
import networkx as nx
import scipy.sparse as sp

#########NEXT SECTION IS ABOUT OWM MODULE
from .get_feature_matrix import get_feature_matrix



"""

Input:

     corr_method: 'jac' or 'cosine'
     alpha: parameter for pagerank
     score_dict_path: path for score dictionary
     prdatafile_path: paths for all pagerank datafiles
     prtagfile_path: paths for all pagerank tagfiles

Main methods:

     run_pagerank: output a dictionary {filename, pagerank score}
     generate_results_summary:  a summarized dataframe for analysis


"""

class chart_ranker():

    def __init__(self, corr_method, alpha, score_dict_path, prdatafile_path, prtagfile_path):


        fm = get_feature_matrix(prdatafile_path, prtagfile_path)
        fm.gen_tag_matrix()
        self.alpha = alpha
        self.feature_matrix = fm.feature_matrix
        with open(score_dict_path, 'rb') as handle:
            self.score_dict = pickle.load(handle)

        self.corr_method = corr_method
        self.filename2score = None
        self.pr = None
        self.pr_results_summary = None
        self.corr_mat = None

    def jac_sim(self, matrix):
        #input matrix a N*D feature matrix, np array
        N = matrix.shape[0]
        sparse = sp.csc_matrix(matrix)
        ab = sparse * sparse.T
        rows_sum = sparse.getnnz(axis=1)
        bb = np.tile(rows_sum, N).reshape(N,N)
        aa = np.repeat(rows_sum,N).reshape(N,N)
        
        return np.array(ab / (aa + bb - ab))


    def cosine_sim(self, matrix):
   
        similarity = np.dot(matrix, matrix.T)
        square_mag = np.diag(similarity)
        inv_square_mag = 1 / square_mag
        inv_square_mag[np.isinf(inv_square_mag)] = 0
        inv_mag = np.sqrt(inv_square_mag)
        cosine = inv_mag.T * inv_mag
        
        return cosine



    def extract_filenamedict(self):

        score_matrix = defaultdict(int)
        for i,(k,v) in enumerate(self.score_dict.items()):
            score_matrix[i] = (k,0.5 * v[0]['top2mean'] + 0.5 * v[1])

        score_table = pd.DataFrame(index = range(0,len(score_matrix)), columns=['File_Name', 'Score'])
        for i,(k,v) in enumerate(self.score_dict.items()):
            #print(i)
            score_table.loc[i, 'File_Name'] = score_matrix[i][0]
            score_table.loc[i, 'Score'] = score_matrix[i][1]

        score_table['Score'] = score_table['Score'].replace(np.nan, score_table['Score'].mean())
        score_table['Score'] = score_table['Score'].apply(lambda x: np.round(x,2))
        self.index2filename = dict(self.feature_matrix['Filename'])
        self.filename2score = pd.Series(score_table['Score'].values, index = score_table['File_Name']).to_dict()


    def get_sim_mat(self, fm, method = 'jac'):
        #fm is a n*n pd dataframe
        if method == 'jac':
            mat = fm.values
            sim_mat = self.jac_sim(mat)

        elif method == 'cosine':
            mat = fm.values
            sim_mat = self.cosine_sim(mat)

        return sim_mat

    def get_pid_filter(self):

        temp_df = self.feature_matrix[['Filename','Pic_ID']]
        temp_df.index = temp_df['Filename']
        temp_df = temp_df.drop('Filename', axis = 1)
        temp_df['dummy'] = np.ones(temp_df.shape[0])

        pidtable = temp_df.pivot(values = 'dummy', columns='Pic_ID')
        pidtable = pidtable.fillna(0)
        pidlayer = pd.DataFrame(np.dot(pidtable,pidtable.transpose()), columns=pidtable.index, index=pidtable.index)
        pidlayer_filter = 1 - pidlayer

        return pidlayer_filter

    def get_corr_matrix(self, corr_method):

        fm = self.feature_matrix.drop(['ClassID', 'Filename','Pic_ID'], 1)
        corr_mat_value = self.get_sim_mat(fm, method = self.corr_method)
        self.corr_mat = pd.DataFrame(corr_mat_value, index=self.feature_matrix['Filename'], columns=self.feature_matrix['Filename'])


    def run_pagerank(self):

        self.extract_filenamedict()
        self.get_corr_matrix(self.corr_method)
        pid_filter = self.get_pid_filter()

        adj_mat = np.multiply(self.corr_mat, pid_filter)
        adj_mat_values = adj_mat.values

        st = time.time()
        g = nx.DiGraph()
        for i,ni in enumerate(adj_mat.index):
            #print(i)
            for j,nj in enumerate(adj_mat.columns):

                if adj_mat_values[i][j] !=0:

                    g.add_edge(ni,nj, weight = adj_mat_values[i][j])

        cost = time.time()- st
        print('Time Cost to build the graph:', cost)

        #run pagerank
        st = time.time()
        self.pr = nx.pagerank_scipy(g, alpha=self.alpha, personalization=self.filename2score, max_iter=300, tol=1.0e-12)
        #print (pr)
        print ('Time Cost to run pagerank:', time.time() - st)



    def generate_results_summary(self, save = True):

        d1 = {k:(v[0]['top2mean'], v[1], v[2]) for k,v in self.score_dict.items()}
        results_df = pd.DataFrame(d1).transpose()
        results_df.columns = ['Interest', 'Importance', 'ClassID']
        file_prscore = pd.Series(self.pr)
        results_df['PR'] = file_prscore
        results_df['PR_Rank'] = results_df['PR'].rank(ascending=False)
        results_df['Pic_ID'] = self.feature_matrix['Pic_ID'].values
        results_df['II'] = results_df['Interest'] + results_df['Importance']
        results_df['II_Rank'] = results_df['II'].rank(ascending=False)

        if save:

            results_df.to_csv('newInterestSc.csv', index = True)

        self.pr_results_summary = results_df