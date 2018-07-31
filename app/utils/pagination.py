from flask import request
from app.mixins.dict import DictMixin

import math

class PaginationHelper(DictMixin):

    def __init__(self, pagination):
        
        self.total_number = pagination.total_number
        self.page = pagination.page
        self.page_size = pagination.page_size
        self.data = pagination.data.to_dict()
        self.last_page = True if math.ceil( self.total_number / self.page_size ) == self.page else False