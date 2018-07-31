from app.utils.email_utility.connection import Connection

from app.utils.email_utility.email_meeting import EmailMeeting
import time
from app.db_models.user import User
from app.services import user_services, meeting_services
from app.ext import raw_db, db
from sqlalchemy.sql import text

connection = Connection('corp\\v803285', '----------', 'mail.statestr.com', 'LXia4@StateStreet.com')

def email_job():

    print("email_job is working")

    items = connection.get_all_unprocessed_meeting_invites()

    # print(items)

    for item in items:
        meeting_invite = EmailMeeting(item)
        # print(meeting_invite)
        organizer = meeting_invite.get_meeting_organizer().email_address
        subject = meeting_invite.get_mail_subject()
        location = meeting_invite.get_meeting_location()
        attendees = meeting_invite.get_meeting_attendees()
        start_time = meeting_invite.get_meeting_start_time()
        end_time = meeting_invite.get_meeting_end_time()
        start_time = time.mktime(start_time.timetuple())
        end_time = time.mktime(end_time.timetuple())

        start_time = time.ctime(start_time)
        end_time = time.ctime(end_time)

        attendees_list = []
        for attendee in attendees:
            attendees_list.append(attendee.mailbox.email_address)

        # sql = 'SELECT * FROM public.user'

        # users = scheduler_db.query(sql)
        # for user in users:
        #     print(user.name)

        with db.app.app_context():

            user_list = User.query.filter(User.email.in_(attendees_list)).filter_by(role_id = 1).all()
            users = [user.id for user in user_list]
            organizer_id = user_services.get_user_id_by_email(organizer)
   
            sql = """SELECT *
                    FROM public.manager_fund mf
                    LEFT JOIN public.user u
                    ON mf.manager_id = u.id
                    where u.email in :lists"""

            # results = db.execute(text(sql), lists = tuple(attendees_list)).fetchall() 

            results = raw_db.query(sql, lists=tuple(attendees_list)).to_dict()

            # print(results)

            meeting_services.save_email_meeting(subject, organizer_id, location, start_time, end_time, results[0].get('fundId'), users)