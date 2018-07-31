del_chart_comment = """
DELETE FROM public.chart_comment
	WHERE id=:id 
"""

query_chart_comment = """
SELECT * FROM (
	SELECT id, chart_id, user_id, comment, create_time, (SELECT name FROM public.user WHERE id = cc.user_id) as user_name
		FROM public.chart_comment cc WHERE chart_id = :chart_id
) c ORDER BY c.create_time DESC, c.id DESC LIMIT :limit OFFSET :offset
"""

query_chart_insight = """
SELECT insight,is_show_original
	FROM public.chart_insight WHERE chart_id = :chart_id AND user_id = :user_id
"""

query_chart_comment_count = """
SELECT COUNT(*)
	FROM public.chart_comment cc WHERE chart_id = :chart_id
"""