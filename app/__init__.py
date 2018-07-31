import logging, pickle, random, copy

from flask import Flask
from config import config
from .ext import db, Api

from app.db_models.alert import Alert

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from app.api_v2 import user_resources as UserResources
from app.api_v2 import heartbeat_resources as HeartbeatResources
from app.api_v2 import analytic_resources as AnalyticResources
from app.api_v2 import asset_resources as AssetResources
from app.api_v2 import intelligent_charts_resources as ChartsResources
from app.api_v2 import alert_resources as AlertResources
from app.api_v2 import report_resources as ReportResources
from app.api_v2 import task_resources as TaskResources
from app.api_v2 import bookmark_resource as BookmarkResource
from app.api_v2 import screen_resources as ScreenResources
from app.api_v2 import collection_resources as CollectionResources
from app.api_v2 import message_resources as MessageResources
from app.api_v2 import test_resources as TestResources
from app.api_v2 import chart_extend_resources as ChartExtendResources
from app.api_v2 import user_entity_resources as UserEntityResources

from app.api_mobile import user_resources as MUserResources
from app.api_mobile import asset_resources as MAssetResources
from app.api_mobile import alert_resources as MAlertResources
from app.api_mobile import task_resources as MTaskResources
from app.api_mobile import meeting_resources as MMeetingResources
from app.api_mobile import intelligent_charts_resources as MChartsResources
from app.api_mobile import report_resources as MReportResources
from app.ext import mc

import os

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.app = app
    db.init_app(app)
    # init APScheduler

    app_logging_configure(app)
    register_api(app)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    @app.before_first_request
    def preprocessing():

        data_path = 'ic_data/v6'
        group_folders = os.listdir(data_path)
        tmp = {}

        for group in group_folders:
            monthly_data = os.listdir(data_path + '/' + group)
            for month in monthly_data:
                files = os.listdir(data_path + '/' + group + '/' + month)
                for file in files:
                    with open(data_path + '/' + group + '/' + month +'/' + file, 'rb') as f:
                        mc[group.lower() + '_' + month + '_' + file.split('.')[0]] = pickle.load(f)

        print('data loading finished')

        # with open('ic_data/v6/General/2017-12/alert_type_dict.pickle', 'rb') as f_s:
        #     alerts = pickle.load(f_s)
        #     for key, value in alerts.items():
        #         for chart_id, info in value.items():
        #             alert = Alert.from_dict(info)
        #             alert.chart_id = chart_id
        #             alert.group_id = 2
        #             alert.alert_threshold_id = key
        #             # alert.alert_type_id = None
        #             alert.description = info.get('narrative')
        #             for entity_id in info.get('entity'):
        #                 alert_clone = copy.deepcopy(alert)
        #                 alert_clone.entity_id = entity_id
        #                 alert_clone.date_key = '2017-12-31'
        #                 db.session.add(alert_clone)

        #     db.session.commit()

        # mc['recommendation'] = AC()._get_ac()

    return app

def app_logging_configure(app):
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def register_api(app):
    api = Api(app = app, prefix = '/api/v2')

    # test function
    api.add_resource(TestResources.TestResource, '/test/db_text')
    api.add_resource(TestResources.ChartTypeResource, '/chart/<type>')
    api.add_resource(TestResources.ChartAsOfDateResource, '/test/chart/asofdate')
    api.add_resource(HeartbeatResources.HeartbeatResource, '/heartbeat')

    # Desktop version api
    # user
    api.add_resource(UserResources.UserListResource, '/users')
    api.add_resource(UserResources.UserResource, '/users/profile')
    api.add_resource(UserResources.LoginResource, '/users/login')
    api.add_resource(UserResources.LogoutResource, '/users/logout')
    api.add_resource(UserResources.UserDetialResource, '/user/detail')
    api.add_resource(UserResources.UserActiveResource, '/users/active','/users/active/<user_id>')
    api.add_resource(UserResources.UserSearchResource, '/users/search')
    api.add_resource(UserResources.UserGroupResource, '/groups')
    api.add_resource(UserEntityResources.UserEntityListResource, '/users/user_entity/<user_id>', '/users/user_entity')

    # analytic
    api.add_resource(AnalyticResources.AnalyticResource, '/analytics/<id>')
    api.add_resource(AnalyticResources.DashboardThumbnailResource, '/dashboard/<dashboard_id>/thumbnail')

    # asset
    api.add_resource(AssetResources.AssetResource,'/assets_map')
    api.add_resource(AssetResources.EntityResource,'/entities')
    
    # alerts
    api.add_resource(AlertResources.AlertListResource, '/alerts')
    api.add_resource(AlertResources.AlertResource, '/alert/<alert_id>')
    api.add_resource(AlertResources.AlertPageResource, '/alert/<alert_id>/page')
    api.add_resource(AlertResources.AlertsMapResource, '/alerts_map')
    api.add_resource(AlertResources.AlertSettingListResource, '/alert/settings')
    api.add_resource(AlertResources.AlertSettingResource, '/alert/setting/<id>')
    api.add_resource(AlertResources.AlertTemplateListResource, '/alert/templates')
    # intelligent chart
    # api.add_resource(ChartsResources.IntelligentChartsResource, '/intelligent_chart/<entity_id>/<chart_id>')
    api.add_resource(ChartsResources.IntelligentChartListResource, '/intelligent_charts')
    api.add_resource(ChartsResources.IntelligentChartResource, '/intelligent_chart/<chart_id>')
    api.add_resource(ChartsResources.IntelligentChartsListInDetailResource, '/intelligent_charts_in_detail')

    #chart extend
    api.add_resource(ChartExtendResources.ChartCommentListResource, '/intelligent_chart/<chart_id>/comments')
    api.add_resource(ChartExtendResources.ChartInsightListResource, '/intelligent_chart/<chart_id>/insights')
    
    # report
    api.add_resource(ReportResources.ReportListResource, '/reports')
    api.add_resource(ReportResources.WorkbenchCollectionListResource, '/reports/collections')
    api.add_resource(ReportResources.ReportResource, '/report/<id>')
    api.add_resource(ReportResources.ReportEditResource, '/report/<id>/edit')
    api.add_resource(ReportResources.ScheduledReportListResource, '/templates/<template_id>/reports')
    api.add_resource(ReportResources.ReportTemplateResource, '/report_template/<report_id>')
    api.add_resource(ReportResources.ReportThumbnailResource, '/report/<report_id>/thumbnail')

    # task
    api.add_resource(TaskResources.TaskListResource, '/tasks')
    api.add_resource(TaskResources.TaskResource, '/task/<task_id>')
    api.add_resource(TaskResources.TaskCloseResource, '/task/<task_id>/close')
    api.add_resource(TaskResources.CommentListResource, '/task/<task_id>/comments')
    api.add_resource(TaskResources.ReplyListResource, '/task/<task_id>/comment/<comment_id>/replies')
    api.add_resource(TaskResources.CommentResource, '/task/<task_id>/comment/<comment_id>')
    api.add_resource(TaskResources.ReplyResource, '/task/<task_id>/comment/<comment_id>/reply/<reply_id>')
    api.add_resource(TaskResources.TaskListInSocialResource, '/social/tasks')
    api.add_resource(TaskResources.TaskAssigneesForPC, '/assignees')
    api.add_resource(TaskResources.UserTaskResource, '/user_task/<task_id>')

    # multiple screen
    api.add_resource(ScreenResources.ScreenListResource, '/screens')
    api.add_resource(ScreenResources.ScreenResource, '/screen/<screen_id>')
    api.add_resource(ScreenResources.ScreenshotResource, '/screenshot/<screenshot_name>')
    # bookmark
    api.add_resource(BookmarkResource.BookmarkListResource, '/bookmarks')
    api.add_resource(BookmarkResource.BookmarkResource, '/bookmark/<bookmark_id>')

    # collection 
    api.add_resource(CollectionResources.CollectionListResource, '/collections')
    api.add_resource(CollectionResources.CollectionResource, '/collection/<collection_id>', '/collection/batch')
    api.add_resource(CollectionResources.CollectionItemListResource, '/collection/<collection_id>/collection_items')
    api.add_resource(CollectionResources.CollectionItemResource, '/collection_item/<collection_item_id>')

    # message
    api.add_resource(MessageResources.MessageListResource, '/messages','/messages/<status>')
    api.add_resource(MessageResources.MessageResource, '/message/<id>/<status>', '/messages/count')

    # mobile api
    #user

    api.add_resource(MUserResources.MUserProfileResources, '/m/users/profile')

    # assets

    api.add_resource(MAssetResources.MAssetResource, '/m/assets/insights')
    api.add_resource(MAssetResources.MAssetStatisticsResources, '/m/assets/statistics')
    api.add_resource(MAssetResources.MAssetLevelResource, '/m/assets/levels/<level>')
    api.add_resource(MAssetResources.MEntityResource, '/m/assets/entity/<entity_id>')
    api.add_resource(MAssetResources.MFundsInEntityResource, '/m/entity/<entity_id>/funds')

    # alert
    api.add_resource(MAlertResources.MAlertListResource, '/m/alerts')
    api.add_resource(MAlertResources.MAlertResource, '/m/alert/<alert_id>')

    # meeting
    api.add_resource(MMeetingResources.MMeetingListResource, '/m/meetings')

    # task
    api.add_resource(MTaskResources.MTaskListResource, '/m/tasks')
    api.add_resource(MTaskResources.MAssgineeResource, '/m/assignees')
    api.add_resource(MTaskResources.MTaskResource, '/m/task/<task_id>')
    api.add_resource(MTaskResources.MCloseTaskResource, '/m/task/<task_id>/close')
    api.add_resource(MTaskResources.MCommentListResource, '/m/task/<task_id>/comments')
    api.add_resource(MTaskResources.MReplyListResource, '/m/task/<task_id>/comment/<comment_id>/replies')

    #report
    api.add_resource(MReportResources.MReportResource, '/m/report/<report_id>')

    # chart
    api.add_resource(MChartsResources.MIntelligentChartResource, '/m/charts/<chart_id>')

