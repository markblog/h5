import os
from flask import send_file, current_app

from app.db_models.report import Report
from app.utils.decorators import auth
from app.utils.patch import BasicResource

class MReportResource(BasicResource):

    @auth
    def get(self, report_id):

        root_path = os.path.dirname(current_app.instance_path)
        report = Report.query.filter_by(id = report_id).first()
        response = send_file(root_path + '/' + report.path, mimetype = 'application/pdf')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
