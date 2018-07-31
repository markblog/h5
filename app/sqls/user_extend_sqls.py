get_entity_set_id = """
SELECT id FROM public.entity_set WHERE group_id = :group_id ORDER BY date_key DESC
"""

get_user_entity = """
SELECT entity_id
	FROM public.user_entity WHERE set_id = :set_id AND user_id = :user_id
"""

get_structure_id = """
SELECT  distinct(entity_id) FROM public.structure WHERE set_id = :set_id
"""

get_entity = """
SELECT * FROM (
	SELECT *, 1 as access FROM public.entity WHERE id in :list1
	UNION
	SELECT *, 0 as access FROM public.entity WHERE id in :list2
) c order by c.name asc LIMIT :limit OFFSET :offset
"""

get_entity_search = """
SELECT * FROM (
	SELECT *, 1 as access FROM public.entity WHERE id in :list1
	UNION
	SELECT *, 0 as access FROM public.entity WHERE id in :list2
) c WHERE c.name LIKE :search1 or c.name LIKE :search2 order by c.name asc LIMIT :limit OFFSET :offset
"""

get_entity_search_count = """
SELECT COUNT(*) FROM (
	SELECT *, 1 as access FROM public.entity WHERE id in :list1
	UNION
	SELECT *, 0 as access FROM public.entity WHERE id in :list2
) c WHERE c.name LIKE :search1 or c.name LIKE :search2
"""

delete_user_entity = """
DELETE FROM public.user_entity WHERE user_id = :user_id AND entity_id = :entity_id
"""

delete_user_entity_all = """
DELETE FROM public.user_entity WHERE user_id = :user_id AND set_id = :set_id
"""

select_by_parent_id_and_set_id = """
SELECT * FROM "public"."structure" WHERE parent_id = :parent_id AND set_id = :set_id
"""

select_structure_by_parent_id = """
SELECT * FROM "public"."structure" WHERE entity_id = :entity_id AND set_id = :set_id
"""