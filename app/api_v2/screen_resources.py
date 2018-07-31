import os
from flask import request, g, current_app, send_file

from app.utils.patch import BasicResource
from app.utils.decorators import auth
from app.services import screen_services

class ScreenListResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self):

        page = request.args.get('page', default = 1, type = int)
        page_size = request.args.get('page_size', default = 6, type = int)
        screens, counts = screen_services.get_screens(page, page_size)
        res = {
            'screens': screens.to_dict(),
            'counts': counts
        }
        return res

    @auth
    def post(self):
        # to get the latest date

        screen = screen_services.create_screen()
        return 'screenshot info has been saved', 201

    @auth
    def delete(self):

        screen_services.delete_all_screens()
        return 'All cleared'

class ScreenResource(BasicResource):
    """docstring for AssetResource"""
    @auth
    def get(self, screen_id):

        screen = screen_services.get_screen_by_id(screen_id)

        return screen.to_dict()

    @auth
    def delete(self, screen_id):

        screen_services.delete_screen(screen_id)

        return 'screen deleted'


class ScreenshotResource(BasicResource):

    @auth
    def get(self, screenshot_name):

        root_path = os.path.dirname(current_app.instance_path)
        response = send_file(root_path + '/screenshots/' + str(g.user.id) + '/' + screenshot_name , mimetype = 'image/gif')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        

