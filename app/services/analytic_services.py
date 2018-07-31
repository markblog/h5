from flask import g

from app.db_models.asset import Structure
from app.db_models.dashboard import Dashboard
from app.ext import raw_db
from app.sqls import analytic_sqls

def get_latest_analytic_by_set(set):
	dashboards = raw_db.query(
						analytic_sqls.get_dashboards_by_set,
						group_id = g.user.group_id, 
						date_key = set.date_key
					)
	return dashboards

def get_latest_analytic_by_entity(id, latest_date):
	dashboards = raw_db.query(
						analytic_sqls.get_dashboards_by_entity,
						entity_id = int(id), 
						date_key = latest_date
					)
	return dashboards

def get_analytic_by_id(id):
	dashboard = raw_db.query(analytic_sqls.get_dashboard_by_id, id = int(id)).first()
	return dashboard

def get_dashboard_id_by_name(name, date_key = '2017-12-31'):
	dashboard = raw_db.query(analytic_sqls.get_dashboard_id_by_name,name = name, date_key = date_key).first()
	return dashboard.id
