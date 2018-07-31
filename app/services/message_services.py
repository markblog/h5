import datetime

from flask import g
from app.ext import raw_db, db
from app.sqls import message_sqls
from app.utils.time_utils import datetime_to_timestamp
from app.db_models.message import Message,MessageType,MessageStatus

def get_messages_by_page(page, page_size):

	parameters = {
        'user_id': g.user.id,
        'offset': (page - 1) * page_size,
        'limit': page_size
	}

	messages = raw_db.query(message_sqls.get_message_by_page, parameters).to_dict()

	for message in messages:
		message_type = message.get('type')
		if message_type == MessageType.TASK.value or message_type == MessageType.COMMENT.value or message_type == MessageType.REPLY.value:
			sql = message_sqls.get_task_name_by_id
		else:
			continue

		entity = raw_db.query(sql, message_entity_id = message.get('messageEntityId')).first()

		if entity:
			entity = entity.to_dict()
			message['name'] = entity.get('name')
		else:
			message['name'] = ''

	return messages

def create_message(parameters):

	message = Message.from_dict(g.args.update(parameters))
	message.from_uid = g.user.id

	db.session.add(message)
	db.session.commit()

def update_all_message(status):

	message_status = MessageStatus[status.upper()]
	raw_db.query(message_sqls.update_all_messages_status, status = message_status.value, user_id = g.user.id)

def update_specific_message(id, status):

	message_status = MessageStatus[status.upper()]
	raw_db.query(message_sqls.update_message_status, status = message_status.value, user_id = g.user.id, message_id = id)


def get_new_message_count():

	count = raw_db.query(message_sqls.get_new_message_count, user_id = g.user.id).first().to_dict()

	return count