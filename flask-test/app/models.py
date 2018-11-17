from app import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text())
    client = db.Column(db.String(24))
    client_priority = db.Column(db.Integer())
    target_date = db.Column(db.DateTime())
    product_area = db.Column(db.String(24))

    def to_json(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client': self.client,
            'client_priority': self.client_priority,
            'target_date': dump_datetime(self.target_date),
            'product_area': self.product_area
        }

    def __repr__(self):
        return '<Feature {}>'.format(self.title)
