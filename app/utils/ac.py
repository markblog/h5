import datetime
from app.libs.ai_lib.chart_caller import acquire_charts


class AC(object):

    def __init__(self):
        self._ac = None
        self._prdatafile_path = 'ic_data/PR_datafiles'
        self._prtagfile_path = 'ic_data/PR_tagfiles'
        self._score_dict_path = 'ic_data/score_dict.pickle'
        self._interest_point_table_path = 'ic_data/df_for_rec.pickle'
        self._thresh_dict_path = 'ic_data/thresh_dict.pickle'
        self._percentile_dict_path = 'ic_data/percentile_dict.pickle'
        self._method = 'jac'
        self._alpha = 0.33
        self._ac = acquire_charts(
            self._method, 
            self._alpha, 
            self._score_dict_path, 
            self._prdatafile_path, 
            self._prtagfile_path, 
            self._interest_point_table_path, 
            self._thresh_dict_path, 
            self._percentile_dict_path
        )
        self._ac.get_all_plot_dict()

    def _get_ac(self):
        # self._generate_alerts()
        return self._ac

    # def _generate_alerts(self):

    #     now we are not support multiple user here, we need add later
    #     from app.components.alerts.models import Alert
    #     from app.ext import db
    #     from config import ALERT_MONITOR

    #     if ALERT_MONITOR:
    #         entity_id = 2
    #         for chart_id in self._ac.get_alert_id():
    #             chart = self._ac.get_charts_details(chart_id)
    #             alert = Alert()
    #             alert.type_id = 2
    #             alert.title = chart.get('title')
    #             alert.description = ','.join(chart.get('alert')[1])
    #             alert.content = chart.get('summary')
    #             alert.chart_id = chart_id
    #             alert.entity_id = entity_id
    #             alert.updated_time = datetime.datetime.utcnow()
    #             alert.group_id = 1
    #             db.session.add(alert)
    #             db.session.flush()

    #         db.session.commit()




