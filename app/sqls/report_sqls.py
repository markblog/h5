get_scheduled_reports_by_page = """
SELECT id, name, updated_time, 3 AS type FROM public.report_template
WHERE user_id = :user_id AND is_delete = False
ORDER BY updated_time DESC
"""
get_one_off_reports_by_page = """
SELECT id, name, updated_time, 2 AS type FROM public.report
WHERE user_id = :user_id AND report_type_id = 2 AND is_delete = False
ORDER BY updated_time DESC
"""
get_all_reports = """
SELECT * FROM (
	SELECT id, name, updated_time, 2 AS type FROM public.report
	WHERE user_id = :user_id AND report_type_id = 2 AND is_delete = False
	UNION
	SELECT id, name, updated_time, 3 AS type FROM public.report_template
	WHERE user_id = :user_id AND is_delete = False
) t
ORDER BY type DESC, updated_time DESC
"""

get_reports_of_template = """
SELECT id, name, updated_time FROM public.report WHERE report_template_id = :template_id AND is_delete = False
ORDER BY updated_time DESC
LIMIT :limit OFFSET :offset
"""

delete_report_template = """
DELETE FROM public.report WHERE report_template_id = :id;
DELETE FROM public.report_template WHERE id = :id;
"""

get_collections_for_workbench = """
SELECT c.id AS collection_id, c.title AS collection_title, ci.charting_data, ci.name, ci.id AS collection_item_id FROM (SELECT id, title, updated_time FROM public.collection WHERE user_id = :user_id AND state = 1 LIMIT :limit OFFSET :offset) c
LEFT JOIN public.collection_item ci ON c.id = ci.collection_id
ORDER BY c.updated_time DESC, ci.date_key DESC
"""

