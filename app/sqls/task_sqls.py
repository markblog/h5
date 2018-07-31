get_all_tasks = """
SELECT t.id, t.title, ut.status, t.updated_time, t.due_date, t.entity, ut.new_reply,
CASE 
	WHEN t.from_uid = ut.user_id THEN False 
	ELSE True
END AS to_me
FROM user_task ut
LEFT JOIN public.task t ON ut.task_id = t.id
WHERE ut.user_id = :user_id
ORDER BY ut.new_reply DESC, ut.status ASC, t.due_date ASC
"""

get_assigned_to_me_task = """
SELECT t.id, t.title, ut.status, t.updated_time, t.due_date, t.entity, ut.new_reply,
CASE 
	WHEN t.from_uid = ut.user_id THEN False 
	ELSE True
END AS to_me
FROM user_task ut
LEFT JOIN public.task t ON ut.task_id = t.id
WHERE ut.user_id = :user_id AND t.from_uid <> :user_id
ORDER BY ut.new_reply DESC, ut.status ASC, t.due_date ASC
"""

get_assigned_by_me_task = """
SELECT t.id, t.title, ut.status, t.updated_time, t.due_date, t.entity, ut.new_reply,
CASE 
	WHEN t.from_uid = ut.user_id THEN False 
	ELSE True
END AS to_me
FROM user_task ut
LEFT JOIN public.task t ON ut.task_id = t.id
WHERE ut.user_id = :user_id AND t.from_uid = :user_id
ORDER BY ut.new_reply DESC, ut.status ASC, t.due_date ASC
"""

get_task_details = """
SELECT t.id, t.title, t.from_uid, t.due_date, t.created_time, t.updated_time, t.description, t.structure_id, t.entity, ut.status, u.name as creator, u.id AS creator_id FROM public.task t
LEFT JOIN public.user u ON t.from_uid = u.id
LEFT JOIN public.user_task ut ON ut.task_id = t.id
WHERE t.id = :task_id AND user_id = :user_id
"""

get_assignees = """
SELECT u.id, u.name FROM public.user_task ut
LEFT JOIN public.user u ON ut.user_id = u.id
WHERE task_id = :task_id AND ut.user_id <> :from_uid
"""

get_notifier = """
SELECT u.id, u.name FROM public.user_task ut
LEFT JOIN public.user u ON ut.user_id = u.id
WHERE task_id = :task_id AND ut.user_id <> :user_id
"""

get_comments_of_tasks = """
SELECT c.created_time, c.content, u.name, c.id AS comment_id, u.id AS user_id FROM public.comment c
LEFT JOIN public.user u ON c.from_uid = u.id
WHERE task_id = :task_id
ORDER BY c.created_time ASC
"""

get_replies_of_comment = """
SELECT r.id AS reply_id, r.content, r.at, u.name, r.created_time, r.comment_id, u.id AS user_id FROM public.reply r
LEFT JOIN public.user u ON u.id = r.from_uid
WHERE comment_id = :comment_id
ORDER BY r.created_time ASC
"""

get_attachments_of_comment = """
SELECT r.id, r.name FROM public.comment_attachment ca
LEFT JOIN public.report r ON ca.attachment_id = r.id
WHERE ca.comment_id = :comment_id
"""

get_task_in_panel = """
SELECT m.content,(SELECT NAME FROM public.user WHERE id = m.from_uid) AS name 
FROM ( 
	(SELECT r.content, r.created_time, r.from_uid 
	 FROM public.reply r,
		(SELECT c.id,c.content,c.created_time 
		 FROM public.comment c
		 WHERE c.task_id = :task_id) a 
	 WHERE r.comment_id=a.id 
	 ORDER BY r.created_time DESC LIMIT 1)
UNION
	(SELECT c.content,c.created_time, c.from_uid
 	 FROM public.comment c
 	 WHERE c.task_id = :task_id
 	 ORDER BY c.created_time DESC LIMIT 1)) m 
 ORDER BY m.created_time DESC LIMIT 1
"""

social_all_tasks = """
SELECT * FROM 
(
	SELECT t.id, t.title, ut.status, t.updated_time, t.due_date, t.entity, ut.new_reply,
	CASE 
		WHEN t.from_uid = ut.user_id THEN False 
		ELSE True
	END AS to_me
	FROM user_task ut
	LEFT JOIN public.task t ON ut.task_id = t.id
	WHERE ut.user_id = :user_id AND ut.status in (1, 2)
	ORDER BY ut.status ASC, t.due_date ASC
) t
ORDER BY updated_time DESC,t.status ASC, t.due_date ASC
LIMIT :limit OFFSET :offset
"""


tasks_search = """
SELECT * FROM 
(
	SELECT t.id, t.title, ut.status, t.updated_time, t.due_date, t.entity, 
	CASE 
		WHEN t.from_uid = ut.user_id THEN False 
		ELSE True
	END AS to_me
	FROM user_task ut
	LEFT JOIN public.task t ON ut.task_id = t.id
	WHERE ut.user_id = :user_id AND ut.status in (1, 2)
	ORDER BY ut.status ASC, t.due_date ASC
) t
WHERE t.title LIKE :search
ORDER BY updated_time DESC
LIMIT :limit OFFSET :offset
"""

fuzzy_matching_pre_assignee = """
SELECT u.name, u.id FROM public.user u WHERE lower(u.name) LIKE :query_string AND u.id not IN :selected_ids
"""

close_task = """
UPDATE public.user_task SET status = 3 WHERE task_id = :task_id
"""


delete_task_all_by_id = """
DELETE FROM public.user_task WHERE task_id = :task_id;
DELETE FROM public.message WHERE type IN (2,3,4) AND message_entity_id = :task_id;
DELETE FROM public.reply WHERE comment_id in (SELECT id FROM public.comment WHERE task_id = :task_id);
DELETE FROM public.comment_attachment WHERE comment_id in (SELECT id FROM public.comment WHERE task_id = :task_id);
DELETE FROM public.comment WHERE task_id = :task_id;
DELETE FROM public.task WHERE id = :task_id;
"""

delete_comment_by_id = """
DELETE FROM public.reply WHERE comment_id = :comment_id;
DELETE FROM public.comment_attachment WHERE comment_id = :comment_id;
DELETE FROM public.comment WHERE id = :comment_id;
"""

delelte_task_by_id = """
DELETE FROM public.task
	WHERE id = :task_id 
"""

delete_comment_by_task_id = """
DELETE FROM public.comment WHERE task_id = :task_id
"""

delete_comment_attachment_by_task_id = """
DELETE FROM public.comment_attachment WHERE id in :ids
"""

get_comment_id_by_task_id = """
SELECT id FROM public.comment WHERE task_id = :task_id
"""
update_new_reply_status_when_comment = """
UPDATE public.user_task SET new_reply = True WHERE task_id = :task_id AND user_id <> :user_id
"""

update_new_reply_status_when_reply = """
UPDATE public.user_task SET new_reply = True WHERE task_id = :task_id AND user_id IN :user_ids
"""
