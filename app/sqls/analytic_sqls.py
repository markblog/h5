get_dashboards_by_entity = """
SELECT df.id, filters, d.name, d.path, d.site_root, d.thumbnail
FROM public.dashboard_filtered df
LEFT JOIN public.dashboard d ON df.dashboard_id = d.id
WHERE entity_id = :entity_id AND date_key = :date_key
ORDER BY d.id ASC
"""

get_dashboards_by_set = """
SELECT df.id, filters, d.name, d.path, d.site_root, d.thumbnail
FROM public.dashboard_filtered df
LEFT JOIN public.dashboard d ON df.dashboard_id = d.id
WHERE group_id = :group_id AND date_key = :date_key AND entity_id is NULL
ORDER BY d.id ASC
"""

get_dashboard_by_id = """
SELECT df.id, filters, d.name, d.path, d.site_root, d.thumbnail
FROM public.dashboard_filtered df
LEFT JOIN public.dashboard d ON df.dashboard_id = d.id
WHERE df.id = :id
"""

get_dashboard_id_by_name = """
SELECT id FROM public.dashboard_filtered 
	WHERE dashboard_id = (SELECT id FROM public.dashboard WHERE lower(name) = :name AND date_key = :date_key) AND filters is NULL
"""