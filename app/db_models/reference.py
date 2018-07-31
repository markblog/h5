from app.ext import db

class Metric(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(63))
    period = db.Column(db.String(15))
    data_source = db.Column(db.String(15))


class Sector(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(63))
    level = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)


class Currency(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(63))
    level = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)


class Region(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(63))
    level = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)

