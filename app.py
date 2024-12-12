from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Category, Product, Cart, CartItem, Order, OrderItem  # Import db from models
from flask_login import login_required, current_user, login_user, LoginManager
from forms import LoginForm
from datetime import datetime

# Initialize the app
app = Flask(__name__)
app.secret_key = "dev-secret"  # Replace with a secure key in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///garden_go.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure the db is initialized with the app context
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def update_last_login():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')

            # Redirect based on user role
            if user.role == 'Admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'Courier':
                return redirect(url_for('courier_dashboard'))
            else:
                return redirect(url_for('show_products'))

        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/show_products')
def show_products():
    products = Product.query.all()
    return render_template("products.html", products=products, user=current_user)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('show_products'))


@app.route('/cart')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('show_products'))

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    total_price = sum(item.quantity * item.product.sell_price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('view_cart'))

    new_quantity = int(request.form.get('quantity', 1))
    if new_quantity < 1:
        db.session.delete(cart_item)
        flash('Item removed from cart.', 'info')
    else:
        cart_item.quantity = new_quantity
        flash('Cart updated.', 'success')

    db.session.commit()
    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('view_cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty. Add some products before checking out.', 'info')
        return redirect(url_for('show_products'))

    # Create the order
    total_price = sum(item.quantity * item.product.sell_price for item in cart.cart_items)
    order = Order(user_id=current_user.id, total_price=total_price, status='Pending')
    db.session.add(order)
    db.session.commit()

    # Add items to the order
    for cart_item in cart.cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.session.add(order_item)
        db.session.delete(cart_item)  # Remove the item from the cart

    # Empty the cart after checkout
    db.session.commit()

    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('order_summary', order_id=order.id))


@app.route('/order/<int:order_id>')
@login_required
def order_summary(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized access to this order.', 'danger')
        return redirect(url_for('products'))

    return render_template('order_summary.html', order=order)


# Main entry point
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
