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


# @app.route('/show_products')
# def show_products():
#     products = Product.query.all()
#     return render_template("products.html", products=products, user=current_user)


# @app.route('/show_products', methods=['GET'])
# def show_products():
#     category = request.args.get('category')  # Get category from query params
#     search_query = request.args.get('search')  # Get search query
#     sort_by = request.args.get('sort_by', 'name')  # Default sort by name

#     products_query = Product.query  # Assuming SQLAlchemy

#     # Apply filtering based on category
#     if category:
#         products_query = products_query.filter_by(category=category)

#     # Apply search functionality
#     if search_query:
#         products_query = products_query.filter(
#             Product.name.ilike(f"%{search_query}%") |
#             Product.description.ilike(f"%{search_query}%")
#         )

#     # Apply sorting
#     if sort_by == 'price':
#         products_query = products_query.order_by(Product.selling_price)
#     elif sort_by == 'weight':
#         products_query = products_query.order_by(Product.product_weight)
#     else:
#         products_query = products_query.order_by(Product.name)

#     products = products_query.all()
#     categories = Product.query.with_entities(Product.category).distinct()

#     return render_template('products.html', products=products, categories=categories, user=current_user)


# @app.route('/show_products', methods=['GET'])
# def show_products():
#     category_name = request.args.get('category')  # Get category name from query params
#     search_query = request.args.get('search')  # Get search query
#     sort_by = request.args.get('sort_by', 'name')  # Default sort by name

#     products_query = Product.query  # Assuming SQLAlchemy

#     # Apply filtering based on category
#     if category_name:
#         products_query = products_query.join(Category).filter(Category.category_name == category_name)

#     # Apply search functionality
#     if search_query:
#         products_query = products_query.filter(
#             Product.name.ilike(f"%{search_query}%") |
#             Product.description.ilike(f"%{search_query}%")
#         )

#     # Apply sorting
#     if sort_by == 'price':
#         products_query = products_query.order_by(Product.selling_price)
#     elif sort_by == 'weight':
#         products_query = products_query.order_by(Product.product_weight)
#     else:
#         products_query = products_query.order_by(Product.name)

#     # Fetch filtered, sorted products
#     products = products_query.all()

#     # Fetch distinct categories
#     categories = Category.query.with_entities(Category.category_name).distinct()

#     return render_template('products.html', products=products, categories=categories, user=current_user)


# from flask import jsonify, render_template, request

@app.route('/show_products', methods=['GET'])
def show_products():
    category_name = request.args.get('category')
    search_query = request.args.get('search')
    sort_by = request.args.get('sort_by', 'name')

    products_query = Product.query

    if category_name:
        products_query = products_query.join(Category).filter(Category.category_name == category_name)

    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f"%{search_query}%") |
            Product.description.ilike(f"%{search_query}%")
        )

    if sort_by == 'price':
        products_query = products_query.order_by(Product.selling_price)
    elif sort_by == 'weight':
        products_query = products_query.order_by(Product.product_weight)
    else:
        products_query = products_query.order_by(Product.name)

    products = products_query.all()
    categories = Category.query.with_entities(Category.category_name).distinct()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX
        return render_template('partials/product_grid.html', products=products)

    return render_template('products.html', products=products, categories=categories, user=current_user)


@app.route('/product/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID or return 404
    return render_template('product_details.html', product=product, user=current_user)




@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # Get the quantity from the form
    quantity = int(request.form['quantity'])

    # Get or create the cart
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart:
        cart = Cart(user_id=current_user.user_id)
        db.session.add(cart)
        db.session.commit()

    # Check if the product is already in the cart
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=product.product_id).first()
    if cart_item:
        cart_item.quantity += quantity  # Update the quantity by the user-selected amount
        toast_message = f'Added {quantity} more {product.name} to your cart!'
    else:
        cart_item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=quantity)
        db.session.add(cart_item)
        toast_message = f'{product.name} added to your cart!'

    db.session.commit()

    # Use the toaster-specific flash
    flash(toast_message, 'success')  # Success indicates the type for the toaster
    return redirect(url_for('show_products'))





@app.route('/cart')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('show_products'))

    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    total_price = sum(item.quantity * item.product.selling_price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.user_id:
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
    if cart_item.cart.user_id != current_user.user_id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('view_cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('view_cart'))


# @app.route('/checkout', methods=['GET', 'POST'])
# @login_required
# def checkout():
#     cart = Cart.query.filter_by(user_id=current_user.user_id).first()
#     if not cart or not cart.cart_items:
#         flash('Your cart is empty. Add some products before checking out.', 'info')
#         return redirect(url_for('show_products'))

#     # Create the order
#     total_price = sum(item.quantity * item.product.selling_price for item in cart.cart_items)
#     order = Order(user_id=current_user.user_id, total_price=total_price, status='Pending', assigned_to="3", address=current_user.address, pincode=current_user.pincode, shipping_cost=10)
#     db.session.add(order)
#     db.session.commit()

#     # Add items to the order
#     for cart_item in cart.cart_items:
#         order_item = OrderItem(
#             order_id=order.order_id,
#             product_id=cart_item.product_id,
#             quantity=cart_item.quantity
#         )
#         db.session.add(order_item)
#         db.session.delete(cart_item)  # Remove the item from the cart

#     # Empty the cart after checkout
#     db.session.commit()

#     flash('Your order has been placed successfully!', 'success')
#     return redirect(url_for('order_summary', order_id=order.order_id))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty. Add some products before checking out.', 'info')
        return redirect(url_for('show_products'))

    # Check for product availability in stock
    for cart_item in cart.cart_items:
        product = cart_item.product
        if cart_item.quantity > product.stock_quantity:
            flash(f'Not enough stock for {product.name}. Available stock: {product.stock_quantity}.', 'danger')
            return redirect(url_for('view_cart'))  # Redirect to cart if stock is insufficient

    # Create the order
    total_price = sum(item.quantity * item.product.selling_price for item in cart.cart_items)
    order = Order(
        user_id=current_user.user_id,
        total_price=total_price,
        status='Pending',
        assigned_to="3",  # You can set this based on your logic
        address=current_user.address,
        pincode=current_user.pincode,
        shipping_cost=10
    )
    db.session.add(order)
    db.session.commit()

    # Add items to the order and update stock
    for cart_item in cart.cart_items:
        # Update product stock
        product = cart_item.product
        product.stock_quantity -= cart_item.quantity  # Decrease the stock

        # Add order items
        order_item = OrderItem(
            order_id=order.order_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.session.add(order_item)
        db.session.delete(cart_item)  # Remove the item from the cart

    # Empty the cart after checkout
    db.session.commit()

    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('order_summary', order_id=order.order_id))


@app.route('/order/<int:order_id>')
@login_required
def order_summary(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.user_id:
        flash('Unauthorized access to this order.', 'danger')
        return redirect(url_for('products'))

    return render_template('order_summary.html', order=order)


# Main entry point
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
