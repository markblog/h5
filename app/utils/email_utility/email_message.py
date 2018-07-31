__author__ = 'v635779'

from .email_item import EmailItem

class EmailMessage(EmailItem):

    def __init__(self, item):
        super().__init__(item)

    def get_mail_sender(self):
        return self.item.sender

    def get_mail_to(self):
        return self.item.to_recipients

    def get_mail_cc(self):
        return self.item.cc_recipients

    def get_mail_bcc(self):
        return self.item.bcc_recipients

    def get_mail_author_info(self):
        return self.item.author

    def is_reponse_requested(self):
        return self.item.response_requested


if __name__ == '__main__':
    pass
