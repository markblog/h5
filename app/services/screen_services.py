import datetime

from flask import g, request
from app.ext import raw_db
from app.db_models.screen import Screen
from app.sqls import screen_sqls
from app.ext import db

def create_screen():

    screen = Screen.from_dict(g.args)

    screen.user_id = g.user.id
    screen.created_time = datetime.datetime.utcnow()
    # screen.image_base64 = g.args.get('image_base64')
    db.session.add(screen)
    db.session.commit()

    return screen

def delete_screen(screen_id):

    Screen.query.filter_by(id = screen_id).delete()
    db.session.commit()

def get_screen_by_id(screen_id):

    screen = Screen.query.get(screen_id)

    return screen

def delete_all_screens():

    Screen.query.filter_by(user_id = g.user.id).delete()
    db.session.commit()

def get_screens(page, page_size):

    parameters = {
        'user_id': g.user.id,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    screens = raw_db.query(screen_sqls.get_screens, parameters)
    counts = raw_db.query(screen_sqls.total_counts, parameters).first().count

    return screens, counts