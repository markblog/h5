from app.mixins.dict import DictMixin
import re
from app.services import analytic_services
class BaseChart(DictMixin):
    """
    BaseChart is the class of offering basic skeleton for the specific chart class. 
    """

    def __init__(self):

        self.__title__ = ''
        self.__type__ = ''
        self.__series__ = []
        self.__description__ = ''
        self.__highlight__ = []
        self.__tableau__ = {}

    def as_dict(self):

        dic = {}

        for key, value in self.__dict__.items():
            if key.startswith('__'):
                key = re.sub(r'[\W_]', '', key)
                dic[key] = value
            elif key.startswith('_'):
                pass
            else:
                dic[key] = value

        return dic
    def _parse_header(self, data):
        headers = list(data)
        xAxis = []
        yAxis = []
        for header in headers:
            if header.startswith('X'):
                xAxis.append(header)
            elif header.startswith('Y'):
                yAxis.append(header)
            else:
                raise Exception('TreeMap -- can not process this in _parse_header ' + header)
        return xAxis, yAxis

    def _available_types(self):
        self.available_types = []

    def _set_common_properties(self, data):
        self.__title__ = data.get('title','No title')
        self.__shortTitle__ = data.get('short_title','No description')
        self.__summary__ = data.get('narrative_insight')
        self.__details__ = data.get('narrative')
        self.__highlight__ = data.get('highlight', [])
        self.__alert__ = None

        self.__filters__ = self._get_filters(data)

        # set available types for each chart
        self._available_types()

        try:
            self.__tableau__['dashboardId'] = analytic_services.get_dashboard_id_by_name(data.get('tableau_info').get('tableau_dashboard'))
        except Exception as e:
            print("**** ",e," ****")

    def _check_pivot(self, data):

        if data.get('pivot'): 

            pass


    def _normalize_weight(self, values):
        sum_values = sum(abs(float(value)) for value in values)
        weights = [ round(abs(float(value))/sum_values * 100) for value in values ]
        return weights

    def _date_formatter(self, dates):
        # date format: 2016-03-31 00:00:00
        return [date[:10] for date in dates]

    def transformation(self):

        raise "Not implemented"

    def _sort_list_preserving_order(self, seq): 
        # order preserving
        checked = []
        for e in seq:
            if e not in checked:
                checked.append(e)
        return checked

    def _get_filters(self, data):

        tags = data.get('tags')
        filters = []
        for key, value in tags.items():
            filters.append({
                    'name': key,
                    'specificFilters': value,
                    'count': len(value)
                })

        return filters

