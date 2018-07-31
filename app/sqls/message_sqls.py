get_message_by_page = """
SELECT * FROM(
	SELECT id, content, created_time,status,to_uid,from_uid,type,message_entity_id 
	FROM public.message 
	WHERE status in (1, 2) AND to_uid=:user_id 
	ORDER BY status, created_time DESC
) m LIMIT :limit OFFSET :offset
"""

get_entity_name_by_id = """
SELECT name FROM public.entity WHERE id=:message_entity_id 
"""

get_task_name_by_id = """
SELECT title as name FROM public.task WHERE id=:message_entity_id
"""

get_new_message_count = """
SELECT COUNT(*)
	FROM public.message 
	WHERE status=1 AND to_uid=:user_id
"""

update_message_status = """
UPDATE public.message SET status= :status WHERE id = :message_id AND to_uid=:user_id
"""

update_all_messages_status = """
UPDATE public.message SET status= :status WHERE to_uid=:user_id AND status IN (1,2)
"""