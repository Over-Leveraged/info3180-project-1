from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Property(db.Model):

    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(555), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(80), nullable=False)
    file_name = db.Column(db.String(80), nullable=False)

    def __init__(self, title, description, bedrooms, bathrooms, location, price, property_type, file_name):
        self.title = title
        self.description = description
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.location = location
        self.price = price
        self.property_type = property_type
        self.file_name = file_name


