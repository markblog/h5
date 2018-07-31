import os
from flask import request,current_app,send_file

from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import report_services
from app.db_models.report import ReportType, Report

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('html')
parser.add_argument('data')
parser.add_argument('type')
parser.add_argument('frequency')


class ReportListResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):
        # to get the latest date
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 6, type = int)
        type = request.args.get('type', default = 1, type = int)

        report_type = ReportType(type)

        return report_services.get_reports_by_type_and_page(report_type.value, page, page_size)


    @auth
    def post(self):

        args = parser.parse_args()

        type = args.get('type', 2)

        try:
            if int(type) == ReportType.ONEOFF.value: 
                report_services.generate_pdf_report(args.get('name'), args.get('html'), args.get('data'), type)
            elif int(type) == ReportType.SCHEDULED.value:
                report_services.generate_pdf_report_and_template(args.get('name'), args.get('html'), args.get('data'), args.get('frequency'))
            else:
                pass

        except Exception as e:
            print(str(e))

        return 'report generated success'


class ScheduledReportListResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self, template_id):
        # to get the latest date
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 5, type = int)

       	reports = report_services.get_reports_of_template(template_id, page, page_size)

        return reports

class ReportEditResource(BasicResource):

    @auth
    def get(self, id):

        type = request.args.get('type', default = 2, type = int)

        if type == ReportType.ONEOFF.value:
            report = report_services.get_report_by_id(id)
            report_dict = report.to_dict()
        elif type == ReportType.SCHEDULED.value:
            report = report_services.get_report_template_by_id(id)
            # to keep consistent with oneoff report, here we have changed the field template to data
            report_dict = report.to_dict()
            report_dict['data'] = report_dict['template']
        else:
            pass

        return report_dict

class ReportResource(BasicResource):

    @auth
    def get(self, id):
        root_path = os.path.dirname(current_app.instance_path)
        report = Report.query.filter_by(id = id).first()
        response = send_file(root_path + '/' + report.path, mimetype = 'application/pdf')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Cache-Control'] = 'no-cache'
        return response

    @auth
    def delete(self, id):

        type = request.args.get('type',type = int)

        report_services.delete_report(id, type)

        return 'delete success', 200

    @auth
    def put(self, id):

        args = parser.parse_args()
        type = request.args.get('type', default = 2, type = int)

        try:
            if type == ReportType.ONEOFF.value:
                report_services.generate_pdf_report(args.get('name'), args.get('html'), args.get('data'), type, id)
            else:
                report_services.update_report_template(id, args.get('data'))

        except Exception as e:
            print(str(e))

        return 'report updated success'

class WorkbenchCollectionListResource(BasicResource):

    @auth
    def get(self):

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 10, type = int)

        ret = report_services.workbench_collections(page, page_size)

        return ret

class ReportTemplateResource(BasicResource):

    @auth
    def get(self, report_id):

        return report_services.acquireReportTemplate(report_id)

class ReportThumbnailResource(BasicResource):

    @auth
    def get(self, report_id):
        type = request.args.get('type', type = int, default = 2)
        if type == ReportType.ONEOFF.value:
            report = report_services.get_report_by_id(report_id)
        else:
            report = report_services.get_report_template_by_id(report_id)

        root_path = os.path.dirname(current_app.instance_path)
        print(root_path + report.thumbnail)
        response = send_file(root_path + '/' + report.thumbnail , mimetype = 'image/gif')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response