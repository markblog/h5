import os
from flask import request 

from app.utils.patch import BasicResource

class HeartbeatResource(BasicResource):

    def get(self):

        status = {
            'pid': os.getpid(),
            'name': 'ai_pc'
        }
        
        return status