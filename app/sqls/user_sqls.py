
get_users_except_current_user = """
SELECT id, name FROM public.user
WHERE group_id = :group_id AND id <> :user_id
ORDER BY name ASC
"""

get_user_id_by_email = """
SELECT id FROM public.user WHERE email=:email
"""

get_user_detail = """
SELECT email,name,tel,position,
								(SELECT COUNT(*) FROM public.user WHERE group_id = u.group_id) AS COUNT 
FROM public.user u WHERE group_id = :group_id limit 1
"""

get_all_user = """
SELECT id, email, name, tel, about, "position", role_id, group_id, status,created_time FROM (
	SELECT * FROM public."user" WHERE group_id = :group_id
	ORDER BY id ASC
) u LIMIT :limit OFFSET :offset
"""

get_active_from_user = """
SELECT count(*) as count FROM public.user WHERE status = :status AND group_id = :group_id
"""

search_user = """
SELECT * FROM (
	SELECT id, email, name, tel, about, "position", role_id, group_id, status, created_time FROM public.user WHERE (name LIKE :search1 or name LIKE :search2) AND group_id = :group_id
) c LIMIT :limit OFFSET :offset
"""

search_count = """
SELECT count(*) as count FROM public.user WHERE (name LIKE :search1 or name LIKE :search2) AND group_id = :group_id
"""

search_count_activated = """
SELECT count(*) as count FROM public.user WHERE status = :status AND (name LIKE :search1 or name LIKE :search2) AND group_id = :group_id
"""

get_all_count = """
SELECT count(*) as total_users_count FROM public."user" WHERE group_id = :group_id
"""

get_all_group = """
SELECT id,name FROM public.group
"""