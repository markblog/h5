import os, pdfkit, datetime, codecs, json, imgkit

from flask import g, current_app
from collections import defaultdict
from app.ext import raw_db,db
from app.sqls import report_sqls
from app.db_models.report import ReportType, ReportTemplate, Report
from app.db_models.task import CommentAttachment
from app.utils.time_utils import datetime_to_timestamp
from app.utils.pagination import PaginationHelper
from app.services import chart_services

def create_report(type, name, path, thumbnail_path, data, template_id = None):

    report = Report.from_dict({
        'report_type_id': type,
        'name': name,
        'user_id':g.user.id,
        'path': path,
        'thumbnail': thumbnail_path,
        'data': json.loads(data)
    })

    if type == ReportType.SCHEDULED.value:
        report.report_template_id = template_id
        report_template = ReportTemplate.query.get(template_id)
        report_template.thumbnail = thumbnail_path

    report.created_time = datetime.datetime.utcnow()
    report.updated_time = datetime.datetime.utcnow()

    db.session.add(report)
    db.session.commit()

def update_report(name, path, data, id):

    report = Report.query.get(id)

    report.update_dict({
        'name': name,
        'path': path,
        'data': json.loads(data)
    })

    print(report.name)

    report.updated_time = datetime.datetime.utcnow()

    db.session.add(report)
    db.session.commit()

def update_report_template(id, data):

    report_template = ReportTemplate.query.get(id)

    report_template.update_dict({
        'name': name,
        'data': json.loads(data)
    })

    report_template.updated_time = datetime.datetime.utcnow()

    db.session.commit()


def get_report_by_id(id):

    report = Report.query.get(id)

    return report

def get_report_template_by_id(id):

    report = ReportTemplate.query.get(id)

    return report

def get_reports_by_type_and_page(report_type, page, page_size):

    parameters = {
        'user_id': g.user.id,
        'page': page,
        'page_size': page_size
    }

    if report_type == ReportType.ALL.value:
        sql = report_sqls.get_all_reports
    elif report_type == ReportType.ONEOFF.value:
        sql = report_sqls.get_one_off_reports_by_page
    elif report_type == ReportType.SCHEDULED.value:
        sql = report_sqls.get_scheduled_reports_by_page
    else:
        pass

    report_pagination = raw_db.paginate(sql, parameters)

    reports = PaginationHelper(report_pagination).to_dict()

    return reports

def get_reports_of_template(template_id, page, page_size):

    parameters = {
        'template_id': template_id,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    reports = raw_db.query(report_sqls.get_reports_of_template, parameters).to_dict({'updatedTime':datetime_to_timestamp})

    return reports

def delete_report(id, type):

    if type == ReportType.ONEOFF.value:
        report = Report.query.get(id)
        report.is_delete = True
    elif type == ReportType.SCHEDULED.value:
        report_template = ReportTemplate.query.get(id)
        report_template.is_delete = True
        # raw_db.query(report_sqls.delete_report_template, id = id)
    else:
        pass
    db.session.commit()

def workbench_collections(page, page_size):

    parameters = {
        'user_id': g.user.id,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    collection_items = raw_db.query(report_sqls.get_collections_for_workbench, parameters).all()

    res = defaultdict(list)
    id_map = defaultdict()
    ret = []

    for item in collection_items:
        if item.charting_data:
            res[item.collection_title].append({'chartingData':item.charting_data, 'name':item.charting_data.get('title'), 'itemId': item.collection_item_id})
        else:
            res[item.collection_title] = []
            
        id_map[item.collection_title] = item.collection_id

    for key, value in res.items():
        ret.append({
            'charts':value,
            'name': key,
            'id': id_map.get(key)
        })

    return ret

def _report_util(html_path, pdf_path):

    print(html_path)

    configuration = pdfkit.configuration(wkhtmltopdf=current_app.config.get('PDF_TOOL_PATH'))
    options = {
        # 'orientation':'Landscape',

    }
    pdfkit.from_file(html_path, pdf_path + '.pdf', configuration=configuration, options = options)

def _img_util(html_path, pdf_path):
    config = imgkit.config(wkhtmltoimage=current_app.config.get('PDF_IMAGE_PATH'))
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }
    imgkit.from_file(html_path, pdf_path + '.jpg', config=config)


def generate_pdf_report(name, html, data, type, id = None, template_id = None):


    now = datetime.datetime.utcnow()
    report_html_folder = '{}/html/{}/{}/'.format(current_app.config.get('REPORTS_PATH'), g.user.id, now.strftime("%Y-%m-%d"))
    report_pdf_folder = '{}/pdf/{}/{}/'.format(current_app.config.get('REPORTS_PATH'), g.user.id, now.strftime("%Y-%m-%d"))
    if not os.path.exists(report_html_folder):
        os.makedirs(report_html_folder)
    if not os.path.exists(report_pdf_folder):
        os.makedirs(report_pdf_folder)

    with codecs.open(report_html_folder + name + '.html', 'w', encoding='utf-8') as f:
        f.write(html)

    pdf_path = report_pdf_folder + name + '_' + now.strftime("%Y%m%d%H%M%S")
    _report_util(report_html_folder + name + '.html', pdf_path)
    _img_util(report_html_folder + name + '.html', pdf_path)

    if id:
        print(pdf_path)
        update_report(name, pdf_path + '.pdf', data, id)
    else:
        create_report(type, name, pdf_path + '.pdf', pdf_path + '.jpg', data, template_id = template_id)


def generate_pdf_report_and_template(name, html, data, frequency):
    # name = db.Column(db.String(128))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    # updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    # frequency = db.Column(db.Integer, default = 7)
    # current_cycle_left = db.Column(db.Integer, default = 7)
    # template = db.Column(db.JSON)
    report_template = ReportTemplate.from_dict({
                        'name': name,
                        'user_id': g.user.id,
                        'created_time': datetime.datetime.utcnow(),
                        'updated_time': datetime.datetime.utcnow(),
                        'frequency': frequency,
                        'current_cycle_left': frequency,
                        'template': json.loads(data)
                    })
    db.session.add(report_template)
    db.session.commit()

    generate_pdf_report(name, html, data, 3, template_id = report_template.id)


def acquireReportTemplate(report_id):

    report = Report.query.get(report_id)

    reportTemplate = ReportTemplate.query.get(report.report_template_id)

    datajson = reportTemplate.template

    chartData = chart_services.get_chart_details(datajson.get('formatData')[0].get('charts')[0].get('chartingId'), None, 1, 6)

    datajson.get('formatData')[0].get('charts')[0]['chartingData'] = chartData

    reportTemplate.template = datajson

    return reportTemplate.to_dict()
