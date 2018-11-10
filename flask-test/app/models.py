from app import db


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text())
    client = db.Column(db.String(24))
    client_priority = db.Column(db.Integer())
    target_date = db.Column(db.DateTime())
    product_area = db.Column(db.String(24))

    def __repr__(self):
        return '<Feature {}>'.format(self.title)