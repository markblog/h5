get_upcoming_meeting = """
SELECT m.start_time, m.location, e.name, m.id  FROM public.meeting_attendance ma 
LEFT JOIN public.meeting m ON m.id = ma.meeting_id
LEFT JOIN public.entity e ON m.entity_id = e.id
WHERE ma.user_id = :user_id
ORDER BY start_time ASC
LIMIT :limit OFFSET :offset
"""

m_get_attendance_of_meeting = """
SELECT u.name FROM public.meeting_attendance ma
LEFT JOIN public.user u ON ma.user_id = u.id
WHERE ma.meeting_id = :meeting_id
"""

m_get_upcoming_meeting_after_date = """
SELECT m.start_time, m.location, e.name, m.id  FROM public.meeting_attendance ma 
LEFT JOIN public.meeting m ON m.id = ma.meeting_id
LEFT JOIN public.entity e ON m.entity_id = e.id
WHERE ma.user_id = :user_id AND start_time >= :date_key
ORDER BY start_time ASC
LIMIT :limit OFFSET :offset
"""

m_get_first_upcoming_meeting_after_date_by_entity = """
SELECT m.start_time, m.location, e.name, m.id  FROM public.meeting_attendance ma 
LEFT JOIN public.meeting m ON m.id = ma.meeting_id
LEFT JOIN public.entity e ON m.entity_id = e.id
WHERE ma.user_id = :user_id AND start_time >= :date_key AND m.entity_id = :entity_id
ORDER BY start_time ASC
"""