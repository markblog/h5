__author__ = 'v635779'

from exchangelib import DELEGATE, Account, Credentials, Configuration, EWSTimeZone, EWSDateTime
from exchangelib.items import Message, MeetingRequest
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from .email_meeting import EmailMeeting
from pytz import timezone
import imaplib

class Connection:
    '''
    Keeps login info the way Exchange likes it.
     :param
    * username: Usernames for authentication are of one of these forms:
      -WINDOMAIN\\username
    *User Password
    *Exchange Server
    * PrimarySMTPAddress
    example('domain\\v635779','email_address','mail.corp.com','user@address.com')
    '''

    def __init__(self, username, password, server, stmp_address, tz_str = 'Asia/Hong_Kong'):
        self.username = username
        self.password = password
        self.server = server
        self.stmp_address = stmp_address
        self.url = 'https://' + server + '/EWS/Exchange.asmx'
        self.tz = EWSTimeZone.timezone(tz_str)

        self._exchangelib_connection = None
        self._imaplib_connection = None
        self._ews_connection = None

    @property
    def exchangelib_connection(self):
        if not self._exchangelib_connection:
            credentials = Credentials(username =self.username, password = self.password)
            config = Configuration(server = self.server, credentials = credentials)
            self._exchangelib_connection = Account(self.stmp_address, config = config, autodiscover = False, access_type = DELEGATE)

        return self._exchangelib_connection

    @property
    def imaplib_connection(self):
        '''This connection for read and unread function in this component'''
        if not self._imaplib_connection:
            self._imaplib_connection = imaplib.IMAP4_SSL(self.server)
            self._imaplib_connection.login(self.username, self.password)

        return self._imaplib_connection

    @property
    def ews_connection(self):
        '''This connection for sending the meeting invite, which don't support by exchangelib'''
        if not self._ews_connection:
            configuration = ExchangeNTLMAuthConnection(url = self.url, username = self.username, password = self.password)
            self._ews_connection = Exchange2010Service(configuration)

        return self._ews_connection

    def is_meeting_invite(self,item):
        return type(item) is MeetingRequest

    def is_message_email(self, item):
        return type(item) is Message

    def get_unread_count(self):
        return self.exchangelib_connection.inbox.unread_count

    def get_latest_n_emails(self, n):
        return self.exchangelib_connection.inbox.all().order_by('-datetime_received')[:n]

    def get_all_unread_emails(self):
        unread_count = self.get_unread_count()
        return self.get_latest_n_emails(unread_count)

    def get_all_unprocessed_meeting_invites(self):
        items = self.get_all_unread_emails()
        meeting_invites = []
        for item in items:
            if self.is_meeting_invite(item):
                meeting_invites.append(item)

        return meeting_invites

    def change_to_folder(self, folder):
        return self.exchangelib_connection.root.get_folder_by_name(folder)

    def get_mail_by_subject_in_folder(self, subject, folder = 'inbox'):
        item = self.change_to_folder(folder).all().get(subject=subject)
        return item

    def get_mails_by_key_in_folder(self, key, folder='inbox'):
        return self.change_to_folder(folder).filter(subject__icontains = key)

    def get_count_by_key(self, key, folder='inbox'):
        return self.change_to_folder(folder).filter(subject__icontains=contains).count()

    def get_meeting_invite_counts_by_time(self, start, end):
        count = self.exchangelib_connection.calendar.filter(start__range=(
            self.tz.localize(EWSDateTime(start[0], start[1], start[2])),
            self.tz.localize(EWSDateTime(start[0], start[1], start[2]))
        )).all().count()

        return count

    def get_calendar_items(self, start, end):
        items = self.exchangelib_connection.calendar.view(
            start = self.tz.localize(EWSDateTime(start[0], start[1], start[2])),
            end = self.tz.localize(EWSDateTime(start[0], start[1], start[2]))
        )

        return items

    def mark_all_unread_emails_as_read(self):
        connection = self.imaplib_connection
        connection.list()
        connection.select('inbox')
        _, items = connection.search(None, 'UNSEEN')
        for item in items[0].split():
            connection.fetch(item, '(BODY.PEEK[])')
            connection.store(item, '+FLAGS','\Seen')
        print('Finished')

    def send_and_save_common_message(self, subject, body, to):
        try:
            m =Message(
                   account=self.exchangelib_connection,
                   folder =a.sent,
                   subject=subject,
                   body=body,
                   to_recipients=to
                  )
            m.send_and_save()
            print('Your message send success!')
        except Exception:
            print('Please try again!')

    def send_only_common_message(self,subject,body,to,cc):
        try:
            m =Message(
                   account=self.exchangelib_connection,
                   folder =a.sent,
                   subject=subject,
                   body=body,
                   to_recipients=to,
                   cc_recipients=cc
                  )
            m.send()
            print('Your message send success!')
        except Exception:
            print('Please try again!')
    #send a common mail with attachment

    def send_with_attachment(self,subject,body,to,path,cc):
        if os.path.exists(path):
            try:
                item =Message(
                       account=self.exchangelib_connection,
                       folder=a.sent,
                       subject=subject,
                       body=body,
                       to_recipients=to,
                       cc_recipients=cc
                      )
                with open(path, 'rb') as f:
                    binary_file_content =f.read()
                my_file = FileAttachment(name=os.path.basename(path), content=binary_file_content)
                item.attach(my_file)
                item.save()
                item.send_and_save()
                print('Your message send success!')
            except Exception:
                print('Please try again!')
        else:
            print('Please check your path' )

    #send a meeting without an attachment (2017,8,15,15,0,0)
    def send_only_meeting(self,subject,location,body,attendees,start,end):
        try:
            event = self.ews_connection.calendar().new_event(
               subject=subject,
               attendees=attendees,
               location =location,
            )
            event.start=timezone("Etc/GMT+8").localize(datetime(start[0],start[1],start[2],start[3],start[4],start[5]))
            event.end=timezone("Etc/GMT+8").localize(datetime(end[0],end[1],end[2],end[3],end[4],end[5]))
            event.html_body=body
            event.create()
            print('Meeting creat success!')
        except Exception:
            print('Please try again!'
              )

if __name__ == '__main__':
    c = Connection('corp\\v605952', '7ujm^YHN', 'mail.statestr.com', 'YHuang@statestreet.com')
    items = c.get_all_unprocessed_meeting_invites()
    for item in items:
        meeting_invite = EmailMeeting(item)
        print(meeting_invite.get_meeting_organizer().name)
        print(meeting_invite.get_meeting_location())
        print(meeting_invite.get_meeting_attendees())
        print(meeting_invite.get_optional_attendees())
        print(meeting_invite.get_meeting_start_time())
        print(meeting_invite.get_meeting_end_time())

