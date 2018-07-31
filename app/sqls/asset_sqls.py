whole_set_data = """
SELECT t.*, smv.value FROM (
WITH RECURSIVE structure_tree AS (
    SELECT * FROM public.structure WHERE level = 2 AND set_id = :set_id
  UNION
    SELECT s.* FROM structure_tree st
    LEFT JOIN public.structure s ON s.parent_id = st.id
    WHERE s.set_id = :set_id
)
SELECT ep.name as parent_name, e.name as child_name, ep.id as parent_id, e.id as child_id, min(st.id) as structure_id, min(st.level) as level FROM structure_tree st
LEFT JOIN public.entity e ON st.entity_id = e.id
LEFT JOIN public.structure sp ON sp.id = st.parent_id
LEFT JOIN public.entity ep ON sp.entity_id = ep.id
LEFT JOIN public.structure spp ON spp.id = sp.parent_id
GROUP BY parent_name, child_name, ep.id, e.id
) t
LEFT JOIN public.structure_metric_value smv ON smv.structure_id = t.structure_id
WHERE metric_id = :metric_id AND date_key = :date_key
"""

get_whole_set_nodes_order_data = """
SELECT t.* FROM (
	WITH RECURSIVE structure_tree AS (
	    SELECT * FROM public.structure WHERE level = 2 AND set_id = :set_id
	  UNION
	    SELECT s.* FROM structure_tree st
	    LEFT JOIN public.structure s ON s.parent_id = st.id
	    WHERE s.set_id = :set_id
	)
	SELECT epp.name as grand_parent_name, epp.id AS grand_parent_id, ep.name as parent_name, ep.id AS parent_id, e.name as child_name, e.id AS child_id FROM structure_tree st
	LEFT JOIN public.entity e ON st.entity_id = e.id
	LEFT JOIN public.structure sp ON sp.id = st.parent_id
	LEFT JOIN public.entity ep ON sp.entity_id = ep.id
	LEFT JOIN public.structure spp ON spp.id = sp.parent_id
	LEFT JOIN public.entity epp ON epp.id = spp.entity_id
	LEFT JOIN public.structure_metric_value smv ON smv.structure_id = st.id
	WHERE date_key = :date_key AND metric_id = :metric_id
) t
ORDER BY grand_parent_name ASC, parent_name ASC, child_name ASC
"""

get_entity_data = """
SELECT * FROM (
	SELECT * FROM (
		SELECT t.*, smv.value FROM (
			WITH RECURSIVE structure_tree AS (
			    SELECT * FROM public.structure WHERE entity_id = :entity_id AND set_id = :set_id
			  UNION
			    SELECT s.* FROM structure_tree st
			    LEFT JOIN public.structure s ON s.id = st.parent_id
			    WHERE s.set_id = :set_id
			)
		SELECT ep.name as parent_name, e.name as child_name, ep.id as parent_id, e.id as child_id, min(st.id) as structure_id, min(st.level) as level FROM structure_tree st
		LEFT JOIN public.entity e ON st.entity_id = e.id
		LEFT JOIN public.structure sp ON sp.id = st.parent_id
		LEFT JOIN public.entity ep ON sp.entity_id = ep.id
		LEFT JOIN public.structure spp ON spp.id = sp.parent_id
		GROUP BY parent_name, child_name, ep.id, e.id
		ORDER BY parent_name, child_name
		) t
		LEFT JOIN public.structure_metric_value smv ON smv.structure_id = t.structure_id
		WHERE metric_id = :metric_id AND date_key = :date_key AND parent_name IS NOT NULL
	) AS parent

	UNION

	SELECT * FROM (
		SELECT t.*, smv.value FROM (
			WITH RECURSIVE structure_tree AS (
			    SELECT * FROM public.structure WHERE entity_id = :entity_id AND set_id = :set_id
			  UNION
			    SELECT s.* FROM structure_tree st
			    LEFT JOIN public.structure s ON s.parent_id = st.id
			    WHERE s.set_id = :set_id
			)
		SELECT ep.name as parent_name, e.name as child_name, ep.id as parent_id, e.id as child_id, min(st.id) as structure_id, min(st.level) as level FROM structure_tree st
		LEFT JOIN public.entity e ON st.entity_id = e.id
		LEFT JOIN public.structure sp ON sp.id = st.parent_id
		LEFT JOIN public.entity ep ON sp.entity_id = ep.id
		LEFT JOIN public.structure spp ON spp.id = sp.parent_id
		GROUP BY parent_name, child_name, ep.id, e.id
		ORDER BY parent_name, child_name
		) t
		LEFT JOIN public.structure_metric_value smv ON smv.structure_id = t.structure_id
		WHERE metric_id = :metric_id AND date_key = :date_key AND parent_name IS NOT NULL
	) AS child
) t
ORDER BY parent_name ASC, child_name ASC
"""

get_entity_nodes_order_data = """
SELECT * FROM (
	SELECT * FROM (
		SELECT t.* FROM (
			WITH RECURSIVE structure_tree AS (
			    SELECT * FROM public.structure WHERE entity_id = :entity_id AND set_id = :set_id
			  UNION
			    SELECT s.* FROM structure_tree st
			    LEFT JOIN public.structure s ON s.id = st.parent_id
			    WHERE s.set_id = :set_id
			)
		SELECT epp.name as grand_parent_name, epp.id AS grand_parent_id, ep.name as parent_name, ep.id AS parent_id, e.name as child_name, e.id AS child_id FROM structure_tree st
		LEFT JOIN public.entity e ON st.entity_id = e.id
		LEFT JOIN public.structure sp ON sp.id = st.parent_id
		LEFT JOIN public.entity ep ON sp.entity_id = ep.id
		LEFT JOIN public.structure spp ON spp.id = sp.parent_id
		LEFT JOIN public.entity epp ON epp.id = spp.entity_id
		LEFT JOIN public.structure_metric_value smv ON smv.structure_id = st.id
		WHERE date_key = :date_key AND metric_id = :metric_id
		) t
		WHERE parent_name IS NOT NULL AND grand_parent_name IS NOT NULL
	) AS parent

	UNION

	SELECT * FROM (
		SELECT t.* FROM (
			WITH RECURSIVE structure_tree AS (
			    SELECT * FROM public.structure WHERE entity_id = :entity_id AND set_id = :set_id
			  UNION
			    SELECT s.* FROM structure_tree st
			    LEFT JOIN public.structure s ON s.parent_id = st.id
			    WHERE s.set_id = :set_id
			)
		SELECT epp.name as grand_parent_name, epp.id AS grand_parent_id, ep.name as parent_name, ep.id AS parent_id, e.name as child_name, e.id AS child_id FROM structure_tree st
		LEFT JOIN public.entity e ON st.entity_id = e.id
		LEFT JOIN public.structure sp ON sp.id = st.parent_id
		LEFT JOIN public.entity ep ON sp.entity_id = ep.id
		LEFT JOIN public.structure spp ON spp.id = sp.parent_id
		LEFT JOIN public.entity epp ON epp.id = spp.entity_id
		LEFT JOIN public.structure_metric_value smv ON smv.structure_id = st.id
		WHERE date_key = :date_key AND metric_id = :metric_id
		) t
		WHERE parent_name IS NOT NULL AND grand_parent_name IS NOT NULL
	) AS child
) t 
ORDER BY grand_parent_name ASC, parent_name ASC, child_name ASC
"""

get_entity_metric_data = """
SELECT t.entity_id, emv_e.value AS emv,  emv_r.value AS ret FROM (SELECT distinct(entity_id) FROM public.structure WHERE set_id = :set_id) t
LEFT JOIN (SELECT entity_id, value FROM public.entity_metric_value WHERE date_key = :date_key AND metric_id = 1) emv_e ON emv_e.entity_id = t.entity_id
LEFT JOIN (SELECT entity_id, value FROM public.entity_metric_value WHERE date_key = :date_key AND metric_id = :metric_id) emv_r ON emv_r.entity_id = t.entity_id
WHERE emv_e.value IS NOT NULL
"""

# level - 1 just for front-end
fuzzy_entity_name_matching = """
SELECT entity_id, name, t.level - 1 AS level FROM (SELECT DISTINCT(entity_id), level FROM public.structure WHERE set_id = :set_id) t
LEFT JOIN public.entity e ON t.entity_id = e.id
WHERE LOWER(name) LIKE :query_string
"""

m_assets_statistics = """
SELECT count(1),level_name, level FROM
 (SELECT DISTINCT entity_id, level, level_name FROM structure WHERE set_id = :set_id) t 
 GROUP BY level, level_name
 ORDER BY level ASC
"""
m_total_amount = """
SELECT sum(value) AS total_amount FROM public.structure s
LEFT JOIN public.structure_metric_value smv ON smv.structure_id = s.id
WHERE s.set_id = :set_id AND smv.date_key = :date_key AND metric_id = 1 AND s.level = 1
"""

# SELECT e.name, e.id AS entity_id, emv_e.value AS amount, emv_a.value AS absolute_return, emv_ex.value AS excess_return
# FROM (SELECT DISTINCT(st.entity_id) FROM public.structure st WHERE st.level = :level AND st.set_id = :set_id) s
# LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 1 AND date_key=:date_key) emv_e ON emv_e.entity_id = s.entity_id
# LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 4 AND date_key=:date_key) emv_a ON emv_a.entity_id = s.entity_id
# LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 2 AND date_key=:date_key) emv_ex ON emv_ex.entity_id = s.entity_id
# LEFT JOIN public.entity e ON e.id = s.entity_id
# ORDER BY e.name ASC
# LIMIT :limit OFFSET :offset


# SELECT s.id, e.name, e.id AS entity_id, emv_e.value AS amount, smv_a.value AS absolute_return, emv_ex.value AS excess_return
# FROM public.structure s
# LEFT JOIN public.structure_metric_value emv_e ON emv_e.structure_id = s.id
# LEFT JOIN public.structure_metric_value smv_a ON smv_a.structure_id = s.id
# LEFT JOIN public.structure_metric_value emv_ex ON emv_ex.structure_id = s.id
# LEFT JOIN public.entity e ON e.id = s.entity_id
# WHERE s.level = :level AND set_id = :set_id
# AND emv_e.metric_id = 1 AND emv_e.date_key = :date_key
# AND smv_a.metric_id = 4 AND smv_a.date_key = :date_key
# AND emv_ex.metric_id = 2 AND emv_ex.date_key = :date_key
# LIMIT :limit OFFSET :offset
m_assets_level_detail = """
SELECT e.name, e.id AS entity_id, emv_e.value AS amount, emv_a.value AS absolute_return, emv_ex.value AS excess_return
FROM (SELECT DISTINCT(st.entity_id) FROM public.structure st WHERE st.level = :level AND st.set_id = :set_id) s
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 1 AND date_key=:date_key) emv_e ON emv_e.entity_id = s.entity_id
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 4 AND date_key=:date_key) emv_a ON emv_a.entity_id = s.entity_id
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 2 AND date_key=:date_key) emv_ex ON emv_ex.entity_id = s.entity_id
LEFT JOIN public.entity e ON e.id = s.entity_id
WHERE emv_e.value IS NOT NULL
ORDER BY emv_e.value DESC
LIMIT :limit OFFSET :offset
"""
m_assets_level_detail_counts = """
SELECT count(1) AS counts FROM
 (SELECT DISTINCT entity_id FROM structure WHERE set_id = :set_id AND level = :level) t 
"""

# SELECT s.id, e.name, e.id AS entity_id, emv_e.value AS amount, smv_a.value AS absolute_return, emv_ex.value AS excess_return
# FROM public.structure s
# LEFT JOIN public.structure_metric_value emv_e ON emv_e.structure_id = s.id
# LEFT JOIN public.structure_metric_value smv_a ON smv_a.structure_id = s.id
# LEFT JOIN public.structure_metric_value emv_ex ON emv_ex.structure_id = s.id
# LEFT JOIN public.entity e ON e.id = s.entity_id
# WHERE s.id = :id
# AND emv_e.metric_id = 1 AND emv_e.date_key = :date_key
# AND smv_a.metric_id = 4 AND smv_a.date_key = :date_key
# AND emv_ex.metric_id = 2 AND emv_ex.date_key = :date_key

m_entity_detail = """
SELECT e.name, e.id AS entity_id, emv_e.value AS amount, emv_a.value AS absolute_return, emv_ex.value AS excess_return
FROM (SELECT id, name FROM public.entity WHERE id = :entity_id) e
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 1 AND date_key=:date_key) emv_e ON emv_e.entity_id = e.id
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 4 AND date_key=:date_key) emv_a ON emv_a.entity_id = e.id
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 2 AND date_key=:date_key) emv_ex ON emv_ex.entity_id = e.id
ORDER BY e.name ASC
"""

m_top3_holding_funds = """
WITH RECURSIVE structure_tree AS (
    SELECT * FROM public.structure WHERE entity_id = 19
  UNION
    SELECT s.* FROM structure_tree st
    LEFT JOIN public.structure s ON s.parent_id = st.id
)
SELECT e.id, e.name FROM (SELECT DISTINCT(st.entity_id) FROM structure_tree st WHERE level = :lowest_level) t
LEFT JOIN public.entity_metric_value emv_e ON emv_e.entity_id = t.entity_id
LEFT JOIN public.entity e ON t.entity_id = e.id
WHERE emv_e.metric_id = 1 AND emv_e.date_key = :date_key
ORDER BY value DESC LIMIT 3
"""

m_holding_funds = """
WITH RECURSIVE structure_tree AS (
    SELECT * FROM public.structure WHERE entity_id = :id
  UNION
    SELECT s.* FROM structure_tree st
    LEFT JOIN public.structure s ON s.parent_id = st.id
)
SELECT e.name, e.id AS entity_id, emv_e.value AS amount, emv_a.value AS absolute_return, emv_ex.value AS excess_return
FROM (SELECT DISTINCT(entity_id) FROM structure_tree WHERE entity_id IS NOT NULL AND level = :lowest_level) s
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 1 AND date_key=:date_key) emv_e ON emv_e.entity_id = s.entity_id
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 4 AND date_key=:date_key) emv_a ON emv_a.entity_id = s.entity_id
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 2 AND date_key=:date_key) emv_ex ON emv_ex.entity_id = s.entity_id
LEFT JOIN public.entity e ON e.id = s.entity_id
WHERE emv_e.value IS NOT NULL
ORDER BY amount DESC
LIMIT :limit OFFSET :offset
"""

m_holding_funds_counts = """
WITH RECURSIVE structure_tree AS (
    SELECT * FROM public.structure WHERE entity_id = :id
  UNION
    SELECT s.* FROM structure_tree st
    LEFT JOIN public.structure s ON s.parent_id = st.id
)
SELECT count(1) AS counts
FROM (SELECT DISTINCT(entity_id) FROM structure_tree WHERE entity_id IS NOT NULL AND level = :lowest_level) s
LEFT JOIN (SELECT * FROM public.entity_metric_value WHERE metric_id = 1 AND date_key=:date_key) emv_e ON emv_e.entity_id = s.entity_id
WHERE emv_e.value IS NOT NULL
"""

select_structure_by_level = """
SELECT entity_id FROM public.structure WHERE set_id = :set_id AND level = :level
"""
