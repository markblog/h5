from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.utils.records import Database
from sqlalchemy import create_engine

db = SQLAlchemy()
raw_db = Database(db)
# here only can use the raw sql for query or other operations
scheduler_db = Database(create_engine('postgresql://postgres:gxtagging@localhost:5432/ai_dev'))

"""
This should be replaced by the real redis database, so to change it conveniently,
please keep the same grammar with redis
- token_black_list is for logout, due to the defects of the jwt
"""
redis_db = {'token_black_list':[]}
mc = {}
# add db model
from app.db_models import user,asset,reference,dashboard, message, chart, user_extend
from app.db_models import alert, task, meeting, report, screen, bookmark, collection
