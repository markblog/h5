import re
from datetime import date
from app.utils.time_utils import datetime_to_timestamp
from app.utils.records import Record, RecordCollection

def underscore_to_camelcase(variable_name):

    first, *rest = variable_name.split('_')
    return first + ''.join(word.capitalize() for word in rest)


class DictMixin(object):

    """
    add the ability which can get dict from the class and convert attribute name to the camelcase style
    """
    __slots__ = ()

    def to_dict(self, excludes = [], camelcase = True):

        dic = {}
        for key, value in self.__dict__.items():
            if re.match('_[^_]', key) or key in excludes:
                # we don't process the private variables for class
                pass
            else:
                if key.startswith('__'):
                    key = re.sub(r'__', '', key)
                if camelcase:
                    key = underscore_to_camelcase(key)

                if isinstance(value, date):
                    value = datetime_to_timestamp(value)

                if isinstance(value, Record) or isinstance(value, RecordCollection):
                    value = value.to_dict()

                dic[key] = value

        return dic

    @classmethod
    def from_dict(cls, _dict):
        attributes = _dict
        if attributes is None or attributes == '':
            raise ValidationError(cls.__name__ + ' does not have a body')
        instance = cls()
        for key,value in attributes.items():
            if key in dir(cls):
                setattr(instance, key, value)
        return instance

    def update_dict(self, _dict):
        attributes = _dict
        if attributes is None or attributes == '':
            raise ValidationError(self.__name__ + ' does not have a body')
        for key,value in attributes.items():
            if key in dir(self):
                setattr(self, key, value)
