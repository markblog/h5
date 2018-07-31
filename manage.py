#!/usr/bin/env python
import os, random, threading, time, requests

from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import g, render_template
from werkzeug.local import LocalProxy
from flask_cors import CORS
from app.utils.flask_monitors import BehaviorMonitorCommand, Monitor

import inspect

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
CORS(app)
Monitor(app, db = db)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('log_behavior', BehaviorMonitorCommand(db))
from app.api_v2.alert_resources import AlertsMapResource

# ----------  start  ----------
# maps_name = app.url_map._rules_by_endpoint

# current_dir = os.getcwd()
# for k,values in maps_name.items():

#     for v in values:
#         if v.rule.startswith("/api/v2"):
#             request_methods = v.methods
#             try:
#                 request_methods.remove("OPTIONS")
#                 request_methods.remove("HEAD")
#             except Exception as e:
#                 pass
#             test_file_ouput.create_file(current_dir + "\\tests\\demo\\", "test_" + k, v.rule, request_methods)

# ----------   end   ----------

# print(app.url_map._rules_by_endpoint)
# print(inspect.getmembers(app.view_functions['mreplylistresource'].view_class))

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def start_runner():
    def start_loop():
        not_started = True
        time_out_flag = 0
        while not_started and time_out_flag <= 10:
            try:
                r = requests.get('http://127.0.0.1:5000/')
                time.sleep(1)
                time_out_flag += 1
                if r.status_code !=502:
                    not_started = False
            except:
                pass

    thread = threading.Thread(target=start_loop)
    thread.start()

if __name__ == '__main__':
    # start_runner()
    manager.run()
