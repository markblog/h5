# from flask_restful import Resource
from app.mixins.dict import DictMixin
from app.services import analytic_services
from app.services import chart_services

from enum import Enum

class IntelligentChartType(Enum):

	ALL = 1
	PERFORMANCE = 2
	RISK = 3
	COMPLIANCE = 4

class Tab(DictMixin):

	def __init__(self):

		self.tab_title = 'title'
		self.tab_content = 'content'

class AnalyticTab(Tab):

	def __init__(self, default_set, entity_id = None):
		super().__init__()
		self.tab_title = 'Analytics'
		self._get_data(default_set, entity_id)
		
	def _get_data(self, default_set, entity_id):
		if entity_id:
			self.tab_content = analytic_services \
							.get_latest_analytic_by_entity(entity_id, default_set.date_key) \
							.to_dict()
		else:
			self.tab_content = analytic_services.get_latest_analytic_by_set(default_set).to_dict()

class IntelligentChartTabHub(Tab):

	def __init__(self, entity_id = None):
		super().__init__()
		self.tab_title = 'Intelligent Charts'
		self._get_data(type, entity_id)
		
	def _get_data(self, type, entity_id):
		res = []

		for member in list(IntelligentChartType):
			res.append(IntelligentChartTab(member, entity_id).to_dict())

		self.tab_content = res

class IntelligentChartTab(Tab):

	def __init__(self, member, level, page = 1, page_size = 6, entity_id = None, as_of_date = None):
		super().__init__()
		self.tab_title = member.name
		self.tab_content = chart_services.get_intelligent_chart_list(entity_id, level, page, page_size, member.name, as_of_date)