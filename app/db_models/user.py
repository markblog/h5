from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.ext import db
from enum import Enum
import datetime
from app.mixins.dict import DictMixin
from flask import current_app
from app.utils.time_utils import now

class Role(Enum):
    
    ADMIN = 0
    ASSET_OWNER = 1
    MANAGER = 2 


class Group(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))  
        
class User(DictMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    about = db.Column(db.Text())
    position = db.Column(db.Text())
    role_id = db.Column(db.Integer, default = Role.MANAGER.value)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    created_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_time = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    status = db.Column(db.Integer,default = 0)

    @staticmethod
    def generate_fake(count=5):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @property
    def password(self):
        return self.password_hash

    # @property
    # def email(self):
    #     return self.email

    # @email.setter
    # def email(self, email):
    #     self.email = email.lower()

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration = 3600 * 24):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id, 'expire_time':now() + expiration}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            refresh_token_or_not = True if now() + 600 >= data.get('expire_time') else False
        except:
            return None, None
        return User.query.get(data['id']), refresh_token_or_not



class ManagerFund(DictMixin, db.Model):

    __tablename__ = 'manager_fund'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer)
    fund_id = db.Column(db.Integer)