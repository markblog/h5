from flask import g
from app.ext import raw_db, db
from app.sqls import meeting_sqls
from app.utils.time_utils import datetime_to_timestamp

from app.db_models.meeting import Meeting, MeetingAttendance

def get_meetings_by_page(page, page_size):

    parameters = {
        'user_id': g.user.id,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    meetings = raw_db.query(meeting_sqls.get_upcoming_meeting, parameters)

    return meetings

def m_get_meetings_by_page_and_attendance(page, page_size):
    
    meetings = get_meetings_by_page(page, page_size).to_dict({
                'startTime': datetime_to_timestamp
        })

    for meeting in meetings:

        attendance = raw_db.query(meeting_sqls.m_get_attendance_of_meeting, meeting_id = meeting.get('id'))
        meeting['attendance'] = attendance.to_dict()

    return meetings

def m_get_meetings_by_page_and_attendance_after_date(date, page, page_size):
    
    parameters = {
        'user_id': g.user.id,
        'date_key': date,
        'offset': (page - 1) * page_size,
        'limit': page_size
    }

    meetings = raw_db.query(meeting_sqls.m_get_upcoming_meeting_after_date, parameters).to_dict({
                'startTime': datetime_to_timestamp
        })

    for meeting in meetings:

        attendance = raw_db.query(meeting_sqls.m_get_attendance_of_meeting, meeting_id = meeting.get('id'))
        meeting['attendance'] = attendance.to_dict()

    return meetings

def m_get_first_upcoming_meeting_by_entity_id(entity_id, date):

    parameters = {
        'user_id': g.user.id,
        'date_key': date,
        'entity_id': entity_id
    } 
    meeting = raw_db.query(meeting_sqls.m_get_first_upcoming_meeting_after_date_by_entity, parameters)\
                .first()
    if meeting:
        meeting = meeting.to_dict({
                        'startTime': datetime_to_timestamp
                })
        attendance = raw_db.query(meeting_sqls.m_get_attendance_of_meeting, meeting_id = meeting.get('id'))
        meeting['attendance'] = attendance.to_dict()

    return meeting




def save_email_meeting(subject, organizer_id, location, start_time, end_time, fund_id,users):

    meeting_info = {
        "subject": subject,
        "organizer_id": organizer_id,
        "location": location,
        "start_time": start_time,
        "end_time": end_time,
        "fund_id": fund_id
    }

    meeting = Meeting.from_dict(meeting_info)

    db.session.add(meeting)
    db.session.flush()

    for user in users:

        meeting_attendance = MeetingAttendance.from_dict({'meeting_id': meeting.id, 'user_id': user})
        db.session.add(meeting_attendance)

    db.session.commit()
