from flask import request 

from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import bookmark_services


class BookmarkListResource(BasicResource):
    """docstring for BookmarkResource"""
    @auth
    def get(self):

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 9, type = int)

        # result = {}

        # result['bookmarkAlerts'] = bookmark_services.get_bookmarks_alerts(page, page_size)
        # result['bookmarkAsserts'] = bookmark_services.get_bookmarks_asserts(page, page_size)
        # result['bookmarkAnalytics'] = bookmark_services.get_bookmarks_analytics(page, page_size)
        # result['bookmarkReports'] = bookmark_services.get_bookmarks_reports(page, page_size)

        return bookmark_services.get_bookmarks(page, page_size)

    @auth
    def post(self):

        bookmark_services.create_bookmark()
        return 'bookmark created success', 201

class BookmarkResource(BasicResource):
    """docstring for BookmarkResource"""

    @auth
    def delete(self, bookmark_id):

        bookmark_services.delete_bookmark(bookmark_id)
        return 'bookmark delete success', 200