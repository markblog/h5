get_screens = """
SELECT id, type, state, screenshot FROM public.screen WHERE user_id = :user_id
ORDER BY created_time DESC
LIMIT :limit OFFSET :offset
"""

total_counts = """
SELECT count(1) AS count FROM public.screen WHERE user_id = :user_id
"""