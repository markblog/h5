get_alerts_by_page = """
SELECT a.id, a.is_read, a.date_key, a.description AS title, e.name AS entity_name FROM public.alert a 
LEFT JOIN public.entity e ON a.entity_id = e.id
WHERE user_id = :user_id OR group_id = :group_id AND date_key = :date_key
ORDER BY is_read ASC, user_id ASC 
"""

get_alerts_by_page_and_in_entity_ids = """
SELECT a.id, a.is_read, a.date_key, a.description AS title, e.name AS entity_name FROM public.alert a 
LEFT JOIN public.entity e ON a.entity_id = e.id
WHERE user_id = :user_id OR group_id = :group_id AND entity_id in :entity_ids AND date_key = :date_key
ORDER BY is_read ASC, user_id ASC 
"""

get_alerts_entity_id = """
SELECT entity_id FROM public.alert 
WHERE date_key = :date_key AND (group_id = :group_id OR user_id = :user_id)
"""

get_alerts_by_page_and_entity = """
SELECT a.id, a.is_read, a.date_key, a.description AS title, e.name AS entity_name FROM public.alert a 
LEFT JOIN public.entity e ON a.entity_id = e.id
WHERE user_id = :user_id OR group_id = :group_id AND entity_id = :entity_id AND date_key = :date_key
ORDER BY is_read ASC, id DESC 
"""

get_related_alerts = """
SELECT a.id AS alert_id, a.description, e.name AS entity_name, date_key  FROM public.alert a
LEFT JOIN public.entity e ON a.entity_id = e.id
WHERE date_key = :date_key AND alert_type_id = :alert_type_id AND (user_id = :user_id OR group_id = :group_id)
LIMIT 10
"""

get_alerts_of_entity = """
SELECT a.id AS alert_id, a.description, e.name AS entity_name, date_key  FROM public.alert a
LEFT JOIN public.entity e ON a.entity_id = e.id
WHERE date_key = :date_key AND (user_id = :user_id OR group_id = :group_id) AND entity_id =:entity_id
ORDER BY a.id DESC
"""

get_alert_threshold_by_page = """
SELECT * FROM (
	SELECT *
	FROM public.alert_threshold ORDER BY date_key DESC
	) a 
WHERE user_id = :user_id AND activate = 1
ORDER BY id DESC
LIMIT :limit OFFSET :offset
"""

get_latest_date_of_alerts= """
SELECT DISTINCT(date_key) AS date_key
  FROM public.alert WHERE group_id = :group_id ORDER BY date_key DESC LIMIT 1
"""