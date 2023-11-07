from app import db


class Region(db.Model):
    # table name
    __tablename__ = 'region'

    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    region_name = db.Column(db.String(255))

    region_manager = db.Column(db.String(255))
