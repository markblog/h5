# for the keep screen features

import datetime
import base64
import os

from flask import g
from app.ext import db
from enum import Enum
from app.mixins.dict import DictMixin

class ScreenType(Enum):
    
    INTELLIGENT_CHART_DETAILS = 1
    ALERT_DETAILS = 2
    TASK_DETAILS = 3

class Screen(DictMixin, db.Model):
    """docstring for Screen"""

    __tablename__ = 'screen'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, default = ScreenType.INTELLIGENT_CHART_DETAILS.value)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    state = db.Column(db.JSON)
    screenshot = db.Column(db.String(128))

    def save_image(self, file):
        pass

    @property
    def image_base64(self):
        return self.screenshot

    @image_base64.setter
    def image_base64(self, image_base64):

        root_folder = 'screenshots/' + str(g.user.id) + '/'

        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(g.user.id) + '.png'

        with open(root_folder + file_name, "wb") as fh:
            fh.write(base64.decodebytes(image_base64.encode()))

        self.screenshot = file_name