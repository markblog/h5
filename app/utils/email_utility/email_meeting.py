__author__ = 'v635779'
from .email_item import EmailItem
class EmailMeeting(EmailItem):

    def __init__(self, item):
        super().__init__(item)

    def get_meeting_organizer(self):
        return self.item.organizer

    def get_meeting_attendees(self):
        return self.item.required_attendees

    def get_optional_attendees(self):
        return self.item.optional_attendees

    def get_meeting_start_time(self):
        return self.item.start

    def get_meeting_end_time(self):
        return self.item.end

    def get_meeting_location(self):
        return self.item.location

