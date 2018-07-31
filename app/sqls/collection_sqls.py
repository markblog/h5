get_collections_by_page = """
SELECT * FROM (
	SELECT id, user_id, title, created_time, updated_time 
	FROM public.collection WHERE state = 1 and user_id=:user_id
) c LIMIT :limit OFFSET :offset
"""

search_collections = """
SELECT * FROM (
	SELECT id, user_id, title, created_time, updated_time 
	FROM public.collection WHERE state = 1 and user_id=:user_id and title LIKE :search
) c LIMIT :limit OFFSET :offset
"""

get_collection_item_by_collection_id = """
SELECT * FROM (
	SELECT id,charting_data,collection_id,date_key,name
	FROM public.collection_item 
	WHERE collection_id=:collection_id ORDER BY date_key DESC
) c LIMIT :limit OFFSET :offset
"""

batch_delete_collection = """
UPDATE public.collection SET state = :state WHERE id in :ids
"""