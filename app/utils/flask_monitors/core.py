import json
import re, base64
from flask import request, session

def save_user_behavior(db, config):

    path = request.path

    if monitor_rules(path, config.get('EXCLUDE_RULES',[])) and request.method != 'OPTIONS':
        args = json.dumps(request.args)
        form = json.dumps(request.form)
        request_json = json.dumps(request.get_json()) if request.get_json() else {}
        method = request.method
        cookies = process_cookies(config.get('COOKIES',[]))
        # _session = process_session(config.get('SESSION',[]))
        user_id = extract_user_info(request.headers.get('Authorization') or request.args.get('token'))

        commit_log_to_db(db, user_id, method, path, args, request_json, form, cookies)

def extract_user_info(token):
    user_id = -1
    
    try:
        if token:
            user_info_token = token.split('.')[1]
            missing_padding = len(user_info_token) % 4
            if missing_padding != 0:
                user_info_token = user_info_token.encode() + b'='* (4 - missing_padding)
            user_info = base64.decodebytes(user_info_token)
            user_info = json.loads(user_info.decode('utf-8'))
            user_id = user_info.get('id')
    except:
        pass

    return user_id


def monitor_rules(path, regex_rules):
    flag = True
    for rule in regex_rules:
        pattern = re.compile(rule)
        match = pattern.match(path)
        if match:
            flag = False
            break;

    return flag

def process_cookies(key_in_cookies):
    dic = {}
    for key in key_in_cookies:
        dic[key] = request.cookies.get(key, None)

    return json.dumps(dic)

def process_session(key_in_session):
    dic = {}
    for key in key_in_session:
        try:
            dic[key] = session.key
        except Exception:
            dic[key] = None
            print('No ' + key + ' in the session, please log the right parameter.')

    return json.dumps(dic)

def commit_log_to_db(db,user_id, method, path, args, request_json, form, cookies):
    sql = "INSERT INTO user_log (user_id, method, path, args, request_json, form, cookies, date) VALUES ({},'{}','{}','{}','{}','{}','{}',{})".format(user_id, method, path, args, request_json, form, cookies, 'now()')
    try:
        db.engine.execute(sql)
    except Exception as e:
        print('Commit user behavior log to database failed.')
