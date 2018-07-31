from flask import request 

from flask import g
from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import chart_extend_service


class ChartCommentListResource(BasicResource):

    @auth
    def post(self, chart_id):

        chart_extend_service.create_chart_comment(chart_id)

        return 'chart_comment created success', 201

    @auth
    def get(self, chart_id):
        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)

        return chart_extend_service.query_chart_comment(chart_id, page_size, page)


class ChartInsightListResource(BasicResource):

    @auth
    def post(self, chart_id):

        insight = g.args.get('insight')
        is_show_original = g.args.get('is_show_original')

        chart_extend_service.update_chart_insight(chart_id, insight, is_show_original)

        return 'chart_insight update success', 200
