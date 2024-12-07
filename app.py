from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Category, Product  # Import db from models

# Initialize the app
app = Flask(__name__)
app.secret_key = "dev-secret"  # Replace with a secure key in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database and migration
# Remove the redundant db initialization here
migrate = Migrate(app, db)  # Pass the existing db instance

# Ensure the db is initialized with the app context
db.init_app(app)

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
    if product.stock_quantity < quantity:
        flash(f"Insufficient stock for {product.name}. Only {product.stock} left!", "error")
        return redirect(url_for("show_products"))

    # Get the cart from the session
    cart = session["cart"]

    # Check if product is already in the cart
    for item in cart:
        if item["id"] == product.id:
            # Update quantity and stock
            if item["quantity"] + quantity <= product.stock_quantity:
                item["quantity"] += quantity
                product.stock_quantity -= quantity
                db.session.commit()
                flash(f"Added {quantity} more of {product.name} to your cart!", "success")
            else:
                flash(f"Not enough stock for {product.name}. Only {product.stock_quantity} left!", "error")
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
    product.stock_quantity -= quantity
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


@app.route("/update-cart/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    action = request.form.get("action")
    cart = session.get("cart", [])

    for item in cart:
        if item["id"] == product_id:
            if action == "increase":
                if item["quantity"] < Product.query.get(product_id).stock_quantity:
                    item["quantity"] += 1
            elif action == "decrease" and item["quantity"] > 1:
                item["quantity"] -= 1
            break

    session["cart"] = cart
    session.modified = True
    return redirect(url_for("view_cart"))


@app.route("/remove-item/<int:product_id>", methods=["POST"])
def remove_item(product_id):
    cart = session.get("cart", [])
    session["cart"] = [item for item in cart if item["id"] != product_id]
    session.modified = True
    # Restore stock when an item is removed from the cart
    product = Product.query.get(product_id)
    if product:
        for item in cart:
            if item["id"] == product_id:
                product.stock_quantity += item["quantity"]
                db.session.commit()
                break
    return redirect(url_for("view_cart"))


@app.route("/clear-cart")
def clear_cart():
    initialize_cart()
    for item in session["cart"]:
        product = Product.query.get(item["id"])
        if product:
            product.stock_quantity += item["quantity"]  # Restore stock
    db.session.commit()
    session.pop("cart", None)
    flash("Your cart has been cleared!", "info")
    return redirect(url_for("view_cart"))


@app.route("/proceed-to-payment", methods=["GET"])
def proceed_to_payment():
    # Add logic to handle payment
    return render_template("payment.html")


# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
