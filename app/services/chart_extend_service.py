import datetime

from flask import g
from app.sqls import chart_sqls
from app.db_models.chart import ChartInsight, ChartComment
from app.ext import raw_db, db
from app.utils.time_utils import datetime_to_timestamp

def create_chart_comment(chart_id):

	chart_comment = ChartComment.from_dict(g.args)
	chart_comment.chart_id = chart_id
	chart_comment.user_id = g.user.id
	chart_comment.create_time = datetime.datetime.utcnow()
	# print(chart_comment.create_time)
	db.session.add(chart_comment)
	db.session.commit()

def delete_chart_comment(id):

	raw_db.query(chart_sqls.del_chart_comment, {"id": id})

def query_chart_comment(chart_id, page_size, page):

	# print(chart_id,'-',page_size, '-',page)

	parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size,
        'chart_id': chart_id
    }

	result = raw_db.query(chart_sqls.query_chart_comment, parameters)
	total_count = raw_db.query(chart_sqls.query_chart_comment_count, parameters).first()

	result.all()

	data = {
		"comment": result.to_dict(),
		"total_count": total_count.count
	}

	return data

def create_chart_insight():

	chart_insight = ChartInsight.from_dict(g.args)
	chart_insight.user_id = g.user.id

	db.session.add(chart_insight)
	db.session.commit()

def update_chart_insight(chart_id, insight, is_show_original):

	chart_insight = ChartInsight.query.get(chart_id)

	if chart_insight:
		chart_insight.insight = insight
		chart_insight.is_show_original = is_show_original
		chart_insight.update_time = datetime.datetime.utcnow()
	else:
		new_chart_insight = ChartInsight.from_dict(g.args)
		new_chart_insight.user_id = g.user.id
		new_chart_insight.chart_id = chart_id

		db.session.add(new_chart_insight)
	db.session.commit()

def query_chart_insight(chart_id, user_id):

	result = raw_db.query(chart_sqls.query_chart_insight, {"chart_id": chart_id, "user_id": user_id})

	result.all()
	# print(result)
	return result
