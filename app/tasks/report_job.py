import time
from app.ext import raw_db, db
from app.db_models.report import ReportTemplate, Report, ReportType

def reportJob():

	print("start report job ........")

	with db.app.app_context():
		allReoprtTemplate = ReportTemplate.query.all()
		for report in allReoprtTemplate:
			if report.current_cycle_left < 2:
				parameters = {
					'name': report.name,
					'user_id': report.user_id,
					'report_template_id': report.id,
					'report_type_id': ReportType.SCHEDULED.value,
				}
				newReport = Report.from_dict(parameters)

				db.session.add(newReport)
				report.current_cycle_left = report.frequency
			else:
				report.current_cycle_left = report.current_cycle_left - 1
		db.session.commit()
	