__author__ = 'V631932'
import pickle
import itertools


from .chart_ranker import chart_ranker

"""

Input:

     corr_method: 'jac' or 'cosine'
     alpha: parameter for pagerank
     score_dict_path: path for score dictionary
     interest_point_table_path: path for the interest point table
     prdatafile_path: paths for all pagerank datafiles
     prtagfile_path: paths for all pagerank tagfiles

Main methods:

     first_x_chart: return a list of filtered ranked charts
     recommend_chart:  given a chart name , return a list of ranked related charts.


"""


class charts_provider():


    def __init__(self, method, alpha, score_dict_path, prdatafile_path, prtagfile_path, interest_point_table_path):
        #self.PR_score = pd.read_csv("newInterestSc.csv",index_col=0)
        self.prdatafile_path = prdatafile_path
        self.prtagfile_path = prtagfile_path

        cr = chart_ranker(method, alpha, score_dict_path, prdatafile_path, prtagfile_path)
        cr.run_pagerank()
        cr.generate_results_summary()
        self.PR_score = cr.pr_results_summary
        self.PR_score["PR"] = (self.PR_score["PR"] - self.PR_score["PR"].min()) / (self.PR_score["PR"].max() - self.PR_score["PR"].min())
        self.PR_score["FileGroup"] = self.PR_score.index.str.split("_").str[0]
        self.PR_score = self.PR_score.sort_values(["PR"],ascending=False)

        #self.Content_Matrix = pd.read_csv("content_sim_jac.csv",index_col=0)
        self.Content_Matrix = cr.corr_mat
        self.Content_Matrix = (self.Content_Matrix - self.Content_Matrix.min()) / (self.Content_Matrix.max() - self.Content_Matrix.min())

        with open(interest_point_table_path, 'rb') as f:
            self.Interest_Point_table = pickle.load(f)
        #self.Interest_Point_table = df_for_rec
        self.Interest_Point_table = self.Interest_Point_table[self.Interest_Point_table.Point != "NAN"]
        self.Interest_Point_table = self.Interest_Point_table.reset_index()
        self.inverted_index = self.get_inverted_index()

    def maxminscale(self,X):
        return (X - X.min()) / (X.max() - X.min())

    def Content_logic(self,pic_id):
        res = self.maxminscale(self.Content_Matrix[pic_id])
        return res.sort_values(ascending= False)

    def get_inverted_index(self):
        Interest_Point_table = self.Interest_Point_table
        inverted_index = {}
        for i in Interest_Point_table.index:
            if type(Interest_Point_table.iloc[i].Point) == tuple:
                x = Interest_Point_table.iloc[i].Point[0]
                y = Interest_Point_table.iloc[i].Point[1]
                x = x + [y]
                x_length = len(x)
                for n in range(1,x_length + 1):
                    for j in itertools.combinations(x,n):
                        if n == 1:
                            j = j[0]
                            j = [j]
                        else:
                            j = list(j)
                            j.sort()
                        j = tuple(j)

                        if j in inverted_index:
                            inverted_index[j] += [Interest_Point_table.iloc[i].Filename]
                        else:
                            inverted_index[j] = []
                            inverted_index[j] += [Interest_Point_table.iloc[i].Filename]

            if type(Interest_Point_table.iloc[i].Point) == list:
                x = Interest_Point_table.iloc[i].Point
                x_length = len(x)
                for n in range(1,x_length + 1):
                    for j in itertools.combinations(x,n):
                        if n == 1:
                            j = j[0]
                            j = [j]
                        else:
                            j = list(j)
                            j.sort()
                        j = tuple(j)
                        if j in inverted_index:
                            inverted_index[j] += [Interest_Point_table.iloc[i].Filename]
                        else:
                            inverted_index[j] = []
                            inverted_index[j] += [Interest_Point_table.iloc[i].Filename]
        return inverted_index


    def get_interest_point(self,chart_name):
        """
        ::input : chart names
        ::return: list of tuple can be reterived in inverted_index{}
        """
        res = []
        Interest_Point_table = self.Interest_Point_table
        points = Interest_Point_table[Interest_Point_table["Filename"] == chart_name].Point.tolist()
        for point in points:
            if type(point) == tuple:
                temp = point[0] + [point[1]]
                temp.sort()
                temp = tuple(temp)
                if temp not in res:
                    res.append(temp)
            else:
                point.sort()
                temp = tuple(point)
                if temp not in res:
                    res.append(temp)
        return res

    def interest_source_logic(self,chart_name):
        res = []
        #print(chart_name)
        points = self.get_interest_point(chart_name)
        for point in points:
    #         if point in inverted_index:
            res += self.inverted_index[point]
        res = list(set(res))
        res.remove(chart_name)
        return res

    def Content_logic(self,pic_id):
        res = self.maxminscale(self.Content_Matrix[pic_id])
        return res.sort_values(ascending= False)

    def first_x_chart(self):
        """
        ranked_chart_list = PR_score.index.values
        """
        ranked_chart_list = self.PR_score.index.values
        x_chart = []
        relevant_pool = []

        x_chart.append(ranked_chart_list[0])
        relevant_pool += list(self.Content_logic(ranked_chart_list[0]).index.values[:1])
        relevant_pool += self.interest_source_logic(ranked_chart_list[0])

        for index in range(1,len(ranked_chart_list)):
            if ranked_chart_list[index] in relevant_pool:
                x_chart.append(ranked_chart_list[index])
                continue
            else:
                x_chart.append(ranked_chart_list[index])
                relevant_pool += list(self.Content_logic(ranked_chart_list[index]).index.values[:1])
                relevant_pool += self.interest_source_logic(ranked_chart_list[index])
        return x_chart

    def recommend_chart(self,chart_name):
        interest_logic_res = self.interest_source_logic(chart_name)
        content_logic_res = list(self.Content_logic(chart_name).index.values)[1:]
        return interest_logic_res, content_logic_res