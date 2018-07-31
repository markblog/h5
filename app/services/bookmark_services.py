import datetime

from flask import g
from app.ext import raw_db, db
from app.sqls import bookmark_sqls
from app.utils.time_utils import datetime_to_timestamp
from app.db_models.bookmark import Bookmark,BookmarkType

def create_bookmark():

    bookmark = Bookmark.from_dict(g.args)
    db.session.add(bookmark)
    db.session.commit()

def delete_bookmark(bookmark_id):

    bookmark = Bookmark.query.get(bookmark_id)
    bookmark.state = 0
    db.session.commit()

def get_bookmarks_alerts(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    return raw_db.query(bookmark_sqls.get_bookmarks_alerts, parameters).to_dict()

def get_bookmarks_asserts(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    return raw_db.query(bookmark_sqls.get_bookmarks_asserts, parameters).to_dict()

def get_bookmarks_analytics(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    return raw_db.query(bookmark_sqls.get_bookmarks_analytics, parameters).to_dict()

def get_bookmarks_reports(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    return raw_db.query(bookmark_sqls.get_bookmarks_reports, parameters).to_dict({'updatedTime': datetime_to_timestamp})


def get_bookmarks(page, page_size):

    parameters = {
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    bookmarks = raw_db.query(bookmark_sqls.get_all_bookmarks, parameters).to_dict()

    bookmark_results = []

    for bookmark in bookmarks:
        if bookmark.get('type') == BookmarkType.ALERTS.value:
            bookmark_get = raw_db.query(bookmark_sqls.get_bookmarks_alerts_by_bookmark_entity_id, id = bookmark.get('id')).first()
        elif bookmark.get('type') == BookmarkType.ASSETS.value:
            bookmark_get = raw_db.query(bookmark_sqls.get_bookmarks_asserts_by_bookmark_entity_id, id = bookmark.get('id')).first()
        elif bookmark.get('type') == BookmarkType.ANALYTICS.value:
            bookmark_get = raw_db.query(bookmark_sqls.get_bookmarks_analytics_by_bookmark_entity_id, id = bookmark.get('id')).first()
        elif bookmark.get('type') == BookmarkType.REPORTS.value:
            bookmark_get = raw_db.query(bookmark_sqls.get_bookmarks_reports_by_bookmark_entity_id, id = bookmark.get('id')).first()
        else:
            pass

        if bookmark_get:
            if bookmark.get('type') == BookmarkType.REPORTS.value:
                bookmark_results.append(bookmark_get.to_dict({'updatedTime': datetime_to_timestamp}))
            else:
                bookmark_results.append(bookmark_get.to_dict())

    return bookmark_results