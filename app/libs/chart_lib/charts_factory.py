import os
from collections import OrderedDict
from ruamel import yaml

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
	generate the order dictionary loader
	"""

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return yaml.load(stream, OrderedLoader)


def get_config_dict():

    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'charts_router.yml'), 'r') as config_file:
        try:
            config_chart_str = config_file.read()
            config_chart_dict = ordered_load(config_chart_str, Loader=yaml.SafeLoader)

        except yaml.YAMLError as e:
            raise e

    return config_chart_dict.get('charts',None)

class ChartFactory(object):
    """docstring for ChartFactory"""

    def get_chart_instance_with_refection(self,data):
        chart = None
        chart_type = data['type']

        config_chart_dict = get_config_dict()
        chart_module = config_chart_dict[chart_type]
        if chart_module:
            kls = self._get_class(chart_module)
            chart = kls()
        else:
            raise Exception('We do not support this chart type for now')

        return chart


    def _get_class(self, module_name):
        parts = module_name.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
