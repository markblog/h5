
#########NEXT SECTION IS ABOUT OWM MODULE
from .DatafileFormated import DatafileFormated
from . import MeasureFormater

class chart_portraits:
    def __init__(self, percentile_dict_path):
        self.measureformater = MeasureFormater.MeasureFormater(percentile_dict_path)
        self.chart_summary = {}
        self.chart_summary["chart"] = []
        self.chart_summary["measure"] = []
        self.chart_summary["NUM"] = []
        self.chart_summary["submeasure"] = []
        self.chart_summary["content"] = []

    def max_portrait(self, DatafileFormated):
        res = self.measureformater.max(DatafileFormated)
        submeasures = ["X", "Y", "score", "value"]
        for temp in range(0, len(res)):
            for submeasure in range(0, len(submeasures)):
                self.chart_summary["chart"].append(DatafileFormated.chart_name)
                self.chart_summary["measure"].append("MAX")
                self.chart_summary["NUM"].append(temp)
                self.chart_summary["submeasure"].append(submeasures[submeasure])
                self.chart_summary["content"].append(res[temp][submeasure])

    def min_portrait(self, DatafileFormated):
        res = self.measureformater.min(DatafileFormated)
        submeasures = ["X", "Y", "score", "value"]
        for temp in range(0, len(res)):
            for submeasure in range(0, len(submeasures)):
                self.chart_summary["chart"].append(DatafileFormated.chart_name)
                self.chart_summary["measure"].append("MIN")
                self.chart_summary["NUM"].append(temp)
                self.chart_summary["submeasure"].append(submeasures[submeasure])
                self.chart_summary["content"].append(res[temp][submeasure])

    def slope_portrait(self,DatafileFormated):
        res = self.measureformater.slope(DatafileFormated)
        submeasures = ["START_TIME", "END_TIME", "Y", "value","score"]
        for temp in range(0,len(res)):
            for submeasure in range(0, len(submeasures)):
                self.chart_summary["chart"].append(DatafileFormated.chart_name)
                self.chart_summary["measure"].append("SLOPE")
                self.chart_summary["NUM"].append(temp)
                self.chart_summary["submeasure"].append(submeasures[submeasure])
                self.chart_summary["content"].append(res[temp][submeasure])

    def SMO_portrait(self, DatafileFormated):
        res = self.measureformater.smo(DatafileFormated)
        submeasures = ["score", "X", "Y_pos", "Y_neg"]
        for submeasure in range(0, len(submeasures)):
            self.chart_summary["chart"].append(DatafileFormated.chart_name)
            self.chart_summary["measure"].append("SMO")
            self.chart_summary["NUM"].append(0)
            self.chart_summary["submeasure"].append(submeasures[submeasure])
            self.chart_summary["content"].append(res[submeasure])
    #
    def Interval_portrait(self, DatafileFormated):
        res = self.measureformater.interval(DatafileFormated)
        for temp in range(0,len(res)):
            if res[temp][0] in ["Increasing", "Decreasing"]:
                submeasures = ["Monotony_Flag","Y", "Amount"]
                for submeasure in range(0, len(submeasures)):
                    self.chart_summary["chart"].append(DatafileFormated.chart_name)
                    self.chart_summary["measure"].append("Interval")
                    self.chart_summary["NUM"].append(temp)
                    self.chart_summary["submeasure"].append(submeasures[submeasure])
                    self.chart_summary["content"].append(res[temp][submeasure])
            else:
                submeasures = ["Monotony_Flag", "Y",
                               "highest_increase_interval","highest_increase_interval_amount","highest_increase_interval_score"
                               ,"highest_decrease_interval","highest_decrease_interval_amount","highest_decrease_interval_score"
                               ,"longest_increase_interval","longest_increase_interval_amount","longest_increase_interval_score"
                               ,"longest_decrease_interval","longest_decrease_interval_amount","longest_decrease_interval_score"]
                for submeasure in range(0, len(submeasures)):
                    self.chart_summary["chart"].append(DatafileFormated.chart_name)
                    self.chart_summary["measure"].append("Interval")
                    self.chart_summary["NUM"].append(temp)
                    self.chart_summary["submeasure"].append(submeasures[submeasure])
                    self.chart_summary["content"].append(res[temp][submeasure])

    def corr_portrait(self, DatafileFormated):
        res = self.measureformater.correlation(DatafileFormated)
        submeasures = ["Y1", "Y2", "value", "score"]
        for temp in range(0, len(res)):
            for submeasure in range(0, len(submeasures)):
                self.chart_summary["chart"].append(DatafileFormated.chart_name)
                self.chart_summary["measure"].append("CORR")
                self.chart_summary["NUM"].append(temp)
                self.chart_summary["submeasure"].append(submeasures[submeasure])
                self.chart_summary["content"].append(res[temp][submeasure])


    def std_portrait(self, DatafileFormated):
        res = self.measureformater.std(DatafileFormated)
        submeasures = ["Y", "score"]
        for temp in range(0, len(res)):
            for submeasure in range(0, len(submeasures)):
                self.chart_summary["chart"].append(DatafileFormated.chart_name)
                self.chart_summary["measure"].append("STD")
                self.chart_summary["NUM"].append(temp)
                self.chart_summary["submeasure"].append(submeasures[submeasure])
                self.chart_summary["content"].append(res[temp][submeasure])

    def Top_portrait(self, DatafileFormated):
        res = self.measureformater.top(DatafileFormated)
        submeasures = ["Y", "X_pos", "pos_percent","X_neg", "neg_percent"]
        for temp in range(0,len(res)):
            for submeasure in range(0,len(submeasures)):
                self.chart_summary["chart"].append(DatafileFormated.chart_name)
                self.chart_summary["measure"].append("Top")
                self.chart_summary["NUM"].append(temp)
                self.chart_summary["submeasure"].append(submeasures[submeasure])
                self.chart_summary["content"].append(res[temp][submeasure])


