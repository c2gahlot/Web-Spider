from app import db
import datetime


class Link(db.Model):
    """
    Create a Link table
    """
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(60), index=True)
    url = db.Column(db.String(1024), index=True, unique=True)
    status = db.Column(db.Enum('pending', 'parsed'), default='pending')
    parsed_at = db.Column(db.Boolean, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Links: {}>'.format(self.base_url + self.end_point)
