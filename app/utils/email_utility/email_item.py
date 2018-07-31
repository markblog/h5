__author__ = 'v635779'

import os
from exchangelib import Message, FileAttachment, ItemAttachment

class EmailItem:

    def __init__(self, item):
        self.item = item

    def get_mail_mime_content(self):
        return self.item.mime_content

    def get_mail_subject(self):
        return self.item.subject

    def get_mail_body(self):
        return self.item.body

    def get_mail_datetime_sent(self):
        return self.item.datetime_sent

    def get_mail_datetime_created(self):
        return self.item.datetime_created

    def get_mail_datetime_received(self):
        return self.item.received

    def get_mail_last_modified_name(self):
        return self.item.last_modified_name

    def get_mail_last_modified_time(self):
        return self.item.last_modified_time

    def is_read(self):
        return self.item.is_read

    def is_reminder(self):
        return self.item.reminder_is_set

    def getAttachment(self,item,Path_string):
        for attachment in item.attachments:
            if isinstance(attachment,FileAttachment):
                local_path = os.path.join(Path_string, attachment.name)
                with open(local_path, 'wb') as f:
                    f.write(attachment.content)
                    print('Saving attachment to', local_path)
            elif isinstance(attachment, ItemAttachment):
                  if isinstance(attachment.item, Message):
                    print(attachment.item.subject, attachment.item.body)
