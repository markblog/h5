__author__ = 'V631932'

from .chart_caller import acquire_charts
import warnings
warnings.filterwarnings("ignore")

def main():
    prdatafile_path = 'D:\\AI PROJECT_NEWDATA\PR_datafiles'
    # A folder contains all datafiles

    prtagfile_path = 'D:\\AI PROJECT_NEWDATA\PR_tagfiles'
    # A folder contains all tagfiles

    score_dict_path = 'D:\\AI PROJECT_NEWDATA\score_dict.pickle'
    # A pickled dictionary

    interest_point_table_path = 'D:\\AI PROJECT_NEWDATA\df_for_rec.pickle'
    # A pickled dataframe

    method = 'jac'
    # metric for calculating charts similarity

    alpha = 0.33
    # parameter in pagerank model.


    AC = acquire_charts(method, alpha, score_dict_path, prdatafile_path, prtagfile_path, interest_point_table_path)
    AC.get_all_plot_dict()

    """
    Methods: 1. get_related_charts('FileName', 'Number')
                    RETURN: an Ordered dict with key to be filenames of related charts, value chart detail

             2. get_charts_by_page('Page Number', 'Number of charts per page')
                    RETURN: an Ordered dict with key to be filenames of charts in the page, value chart detail
             
             3. get_charts_details('FileName')
                    RETURN : chart detail dictionary

             4. get_first_k_charts('Number')
                    RETURN: an Ordered dict with key to be filenames of charts by rank, value chart detail

    """
    
if __name__ == "__main__":
    main()