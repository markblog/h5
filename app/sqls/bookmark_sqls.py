get_bookmarks_alerts = """
SELECT id,type,bookmark_entity_id,state,(
	SELECT COUNT(*) 
	FROM public.alert 
	WHERE alert_type_id = b.bookmark_entity_id) AS entity_count,
	(	SELECT name 
		FROM  public.alert_type 
		WHERE id=b.bookmark_entity_id) AS name, 
	'Alert' AS title
FROM public.bookmark b
WHERE type=1 AND state=1 
LIMIT :limit OFFSET :offset
"""

get_bookmarks_asserts = """
SELECT id,type,bookmark_entity_id,state,
	(SELECT name FROM public.entity WHERE id=b.bookmark_entity_id) AS name,
	(SELECT 'Assets / '||level_name FROM public.structure WHERE entity_id=b.bookmark_entity_id ) AS title,
	(SELECT value FROM public.structure_metric_value 
		WHERE structure_id=
			(SELECT id FROM structure WHERE entity_id=b.bookmark_entity_id) AND metric_id=1 AND date_key=
				(SELECT MAX(date_key) FROM public.structure_metric_value WHERE structure_id=b.bookmark_entity_id AND metric_id=1)) AS total_amount,
	(SELECT value FROM public.structure_metric_value 
		WHERE structure_id=
			(SELECT id FROM structure WHERE entity_id=b.bookmark_entity_id) AND metric_id=2 AND date_key=
				(SELECT MAX(date_key) FROM public.structure_metric_value WHERE structure_id=b.bookmark_entity_id AND metric_id=2)) AS absolute_return,
	(SELECT value FROM public.structure_metric_value 
		WHERE structure_id=
			(SELECT id FROM structure WHERE entity_id=b.bookmark_entity_id) AND metric_id=4 AND date_key=
				(SELECT MAX(date_key) FROM public.structure_metric_value WHERE structure_id=b.bookmark_entity_id AND metric_id=4)) AS excess_return
FROM public.bookmark b WHERE type=2 AND state=1 
LIMIT :limit OFFSET :offset
"""

get_bookmarks_analytics = """
SELECT id,type,bookmark_entity_id,state, 'Analytics' AS title, 
	(SELECT name FROM public.dashboard WHERE id=b.bookmark_entity_id) 
FROM public.bookmark b 
WHERE type=3 AND state=1 
LIMIT :limit OFFSET :offset
"""

get_bookmarks_reports = """
SELECT id,type,bookmark_entity_id,state,'Report' AS title, 
	(SELECT name FROM report_template WHERE id=b.bookmark_entity_id) AS name, 
	(SELECT updated_time FROM report_template WHERE id=b.bookmark_entity_id) AS updated_time 
FROM public.bookmark b 
WHERE type=4 AND state=1 
LIMIT :limit OFFSET :offset
"""

get_all_bookmarks = """
SELECT * FROM ( 
	SELECT id,type,bookmark_entity_id,state FROM public.bookmark WHERE state=1 
) t LIMIT :limit OFFSET :offset
"""

get_bookmarks_alerts_by_bookmark_entity_id = """
SELECT id,type,bookmark_entity_id,state,(
	SELECT COUNT(*) 
	FROM public.alert 
	WHERE alert_type_id = b.bookmark_entity_id) AS entity_count,
	(	SELECT name 
		FROM  public.alert_type 
		WHERE id=b.bookmark_entity_id) AS name, 
	'Alert' AS title
FROM public.bookmark b
WHERE type=1 AND state=1 AND id=:id
"""

get_bookmarks_asserts_by_bookmark_entity_id = """
SELECT id,type,bookmark_entity_id,state,
	(SELECT name FROM public.entity WHERE id=b.bookmark_entity_id) AS name,
	(SELECT 'Assets / '||level_name FROM public.structure WHERE entity_id=b.bookmark_entity_id ) AS title,
	(SELECT value FROM public.structure_metric_value 
		WHERE structure_id=
			(SELECT id FROM structure WHERE entity_id=b.bookmark_entity_id) AND metric_id=1 AND date_key=
				(SELECT MAX(date_key) FROM public.structure_metric_value WHERE structure_id=b.bookmark_entity_id AND metric_id=1)) AS total_amount,
	(SELECT value FROM public.structure_metric_value 
		WHERE structure_id=
			(SELECT id FROM structure WHERE entity_id=b.bookmark_entity_id) AND metric_id=2 AND date_key=
				(SELECT MAX(date_key) FROM public.structure_metric_value WHERE structure_id=b.bookmark_entity_id AND metric_id=2)) AS absolute_return,
	(SELECT value FROM public.structure_metric_value 
		WHERE structure_id=
			(SELECT id FROM structure WHERE entity_id=b.bookmark_entity_id) AND metric_id=4 AND date_key=
				(SELECT MAX(date_key) FROM public.structure_metric_value WHERE structure_id=b.bookmark_entity_id AND metric_id=4)) AS excess_return
FROM public.bookmark b WHERE type=2 AND state=1 AND id=:id
"""

# get_bookmarks_analytics_by_bookmark_entity_id = """
# SELECT id,type,bookmark_entity_id,state, 'Analytics' AS title, 
# 	(SELECT name FROM public.dashboard WHERE id=b.bookmark_entity_id) 
# FROM public.bookmark b 
# WHERE type=3 AND state=1 AND id=:id
# """
get_bookmarks_analytics_by_bookmark_entity_id = """
SELECT b.id,b.type,b.bookmark_entity_id,b.state,d.type AS title, d.name AS name,d.description
	FROM public.bookmark b 
		LEFT JOIN public.dashboard d 
		ON b.bookmark_entity_id=d.id
WHERE b.type=3 AND b.state=1 AND b.id=:id
"""

get_bookmarks_reports_by_bookmark_entity_id = """
SELECT id,type,bookmark_entity_id,state,'Report' AS title, 
	(SELECT name FROM report_template WHERE id=b.bookmark_entity_id) AS name, 
	(SELECT updated_time FROM report_template WHERE id=b.bookmark_entity_id) AS updated_time 
FROM public.bookmark b 
WHERE type=4 AND state=1 AND id=:id
"""