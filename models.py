from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'  # Matches the foreign key reference 'user'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # String representation for debugging
    def __repr__(self):
        return f"<User {self.username}>"

# Category Model
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_Name = db.Column(db.String(50), nullable=False, unique=True)
    Category_description = db.Column(db.Text, nullable=True)
    product = db.relationship('Product', backref='category', lazy=True)

# Product Model
class Product(db.Model):
    __tablename__ = 'product'  # Explicit table name for clarity

    # Define the primary key column
    id = db.Column(db.Integer, primary_key=True)  # primary_key=True marks this as the primary key
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    stock_quantity = db.Column(db.Integer)
    image_url = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Assuming you have a User model
    user = db.relationship("User", backref=db.backref("carts", lazy=True))
    items = db.relationship("CartItem", backref="cart", lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product", backref=db.backref("cart_items", lazy=True))
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)



# Create database tables if not already created
with app.app_context():
    db.create_all()
