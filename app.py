from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__)
app.secret_key = "dev-secret"  # Replace with a secure key in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)  # Add image_url column


# Cart helper function
def initialize_cart():
    if "cart" not in session:
        session["cart"] = []

# Routes
@app.route("/")
def show_products():
    products = Product.query.all()
    return render_template("products.html", products=products)

@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    initialize_cart()  # Ensure the cart is initialized
    product = Product.query.get_or_404(product_id)  # Fetch the product or 404 if not found
    quantity = int(request.form.get("quantity", 1))  # Default quantity to 1 if not provided

    # Check stock availability
    if product.stock < quantity:
        flash(f"Insufficient stock for {product.name}. Only {product.stock} left!", "error")
        return redirect(url_for("show_products"))

    # Get the cart from the session
    cart = session["cart"]

    # Check if product is already in the cart
    for item in cart:
        if item["id"] == product.id:
            # Update quantity and stock
            item["quantity"] += quantity
            product.stock -= quantity
            db.session.commit()
            flash(f"Added {quantity} more of {product.name} to your cart!", "success")
            session["cart"] = cart
            session.modified = True
            return redirect(url_for("show_products"))

    # Add a new product to the cart
    cart.append({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": quantity,
        "image_url": product.image_url  # Include image URL for later use
    })
    product.stock -= quantity
    db.session.commit()

    session["cart"] = cart
    session.modified = True
    flash(f"{product.name} added to your cart!", "success")
    return redirect(url_for("show_products"))


@app.route("/cart")
def view_cart():
    initialize_cart()
    cart = session["cart"]
    cart_items = []

    for item in cart:
        product = Product.query.get(item["id"])  # Fetch product details from the database
        if product:
            cart_items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item["quantity"],
                "image_url": product.image_url,  # Fetch the image URL
            })

    # Calculate the total price
    total = sum(item["price"] * item["quantity"] for item in cart_items)

    return render_template("cart.html", cart=cart_items, total=total)



@app.route("/clear-cart")
def clear_cart():
    initialize_cart()
    for item in session["cart"]:
        product = Product.query.get(item["id"])
        if product:
            product.stock += item["quantity"]  # Restore stock
    db.session.commit()
    session.pop("cart", None)
    return redirect(url_for("view_cart"))

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
