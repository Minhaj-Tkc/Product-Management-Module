from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    __tablename__ = 'product'  # Explicit table name for clarity

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Product name
    description = db.Column(db.Text, nullable=True)  # Product description
    price = db.Column(db.Float, nullable=False)  # Product price
    stock = db.Column(db.Integer, default=0, nullable=False)  # Stock quantity
    image_url = db.Column(db.String(255), nullable=True)  # Image URL
    category = db.Column(db.String(50), nullable=True)  # Product category
    weight = db.Column(db.Float, nullable=False)  # Product weight

    def __repr__(self):
        return f"<Product {self.name}>"

    def __init__(self, name, description, price, stock, image_url, category, weight):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url
        self.category = category
        self.weight = weight


# Cart Model
class Cart(db.Model):
    __tablename__ = 'cart'  # Explicit table name for clarity

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Foreign key to Product table
    quantity = db.Column(db.Integer, default=1, nullable=False)  # Quantity of the product

    # Relationship to access Product details from Cart
    product = db.relationship('Product', backref=db.backref('carts', lazy=True))

    def __repr__(self):
        return f"<Cart Product ID: {self.product_id}, Quantity: {self.quantity}>"

    def __init__(self, product_id, quantity=1):
        self.product_id = product_id
        self.quantity = quantity


# Create database tables if not already created
with app.app_context():
    db.create_all()
