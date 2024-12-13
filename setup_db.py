from app import app, db  # Import the app and db from your Flask app
from models import Category, Product, User, Cart, Subscription  # Import your models
from werkzeug.security import generate_password_hash
from datetime import datetime

def setup_db():
    with app.app_context():  # Ensure the app context is active
        # Create all tables in the database
        db.create_all()

        # Add categories
        flowers = Category(
            category_name="Flowers", 
            category_description="A variety of beautiful flowers."
        )
        vegetables = Category(
            category_name="Vegetables", 
            category_description="Fresh and organic vegetables."
        )
        herbs = Category(
            category_name="Herbs", 
            category_description="Aromatic and medicinal herbs."
        )

        db.session.add_all([flowers, vegetables, herbs])
        db.session.commit()

        # Add dummy products
        dummy_products = [
            Product(
                name="Rose Plant",
                description="A beautiful red rose plant.",
                cost_price=150,
                selling_price=200,
                category_id=flowers.category_id,
                stock_quantity=50,
                product_weight=0.5,
                image_url="https://bouqs.com/blog/wp-content/uploads/2018/08/shutterstock_1662182848-min-1080x719.jpg"
            ),
            Product(
                name="Tomato Plant",
                description="Healthy tomato plant for fresh produce.",
                cost_price=100,
                selling_price=120,
                category_id=vegetables.category_id,
                stock_quantity=30,
                product_weight=0.8,
                image_url="https://t3.ftcdn.net/jpg/02/71/63/24/360_F_271632489_iZexHnP4LtGvDD39QvklpgrgdMeGj7PH.jpg"
            ),
            Product(
                name="Aloe Vera",
                description="Low-maintenance aloe vera plant with medicinal properties.",
                cost_price=80,
                selling_price=110,
                category_id=herbs.category_id,
                stock_quantity=40,
                product_weight=1.2,
                image_url="https://m.media-amazon.com/images/I/81XWpVvk5AL._AC_UF1000,1000_QL80_.jpg"
            ),
            Product(
                name="Marigold Plant",
                description="Bright yellow marigold plant to beautify your garden.",
                cost_price=50,
                selling_price=75,
                category_id=flowers.category_id,
                stock_quantity=60,
                product_weight=0.4,
                image_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.gardendesign.com%2Fflowers%2Fmarigold.html&psig=AOvVaw1Lnq-ehqiWtVSbfM9myecp&ust=1734197490937000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCMCJoZ6jpYoDFQAAAAAdAAAAABAY"
            ),
            Product(
                name="Spinach Plant",
                description="Nutritious and fresh spinach plant for your kitchen garden.",
                cost_price=30,
                selling_price=50,
                category_id=vegetables.category_id,
                stock_quantity=80,
                product_weight=0.3,
                image_url="https://rukminim2.flixcart.com/image/850/1000/xif0q/plant-sapling/z/s/b/annual-yes-yes-spinach-1-pot-elitegreen-original-imagjpcsgfdjmd6d.jpeg?q=90&crop=false"
            ),
            Product(
                name="Tulsi Plant",
                description="Sacred and medicinal tulsi plant for health benefits.",
                cost_price=60,
                selling_price=90,
                category_id=herbs.category_id,
                stock_quantity=70,
                product_weight=0.6,
                image_url="https://lh3.googleusercontent.com/-HICQiS4SJBEWT8SShC0WTJ4fFBqFK-TPsnaTCCI28DBRkGHq6xQEUbTg3ooKd1LKZAoBot3C-j10VICkpCwOKpRMfQ9y763-Q=w3840-h2160-c-rw-v3"
            )
        ]

        db.session.add_all(dummy_products)
        db.session.commit()

        # Add dummy users
        dummy_users = [
            User(
                name="Admin",
                email="admin@gmail.com",
                password_hash=generate_password_hash("010203"),
                role="Admin",
                created_at=datetime.utcnow()
            ),
            User(
                name="Courier",
                email="courier1@gmail.com",
                password_hash=generate_password_hash("010203"),
                role="Courier",
                phone_number="1234567890",
                vehicle_info="Motorcycle",
                vehicle_number="AB123CD",
                created_at=datetime.utcnow()
            ),
            User(
                name="Courier Two",
                email="courier2@example.com",
                password_hash=generate_password_hash("courierpassword"),
                role="Courier",
                phone_number="1234567891",
                vehicle_info="Bicycle",
                vehicle_number="EF456GH",
                created_at=datetime.utcnow()
            ),
            User(
                name="User",
                email="user@gmail.com",
                password_hash=generate_password_hash("010203"),
                role="Customer",
                phone_number="1234567892",
                address="123 Main Street",
                pincode="560001",
                created_at=datetime.utcnow()
            ),
            User(
                name="Customer Two",
                email="customer2@example.com",
                password_hash=generate_password_hash("customerpassword"),
                role="Customer",
                phone_number="1234567893",
                address="456 Elm Street",
                pincode="560002",
                created_at=datetime.utcnow()
            ),
        ]

        db.session.add_all(dummy_users)
        db.session.commit()

        # Add a subscription for demonstration
        subscription = Subscription(
            user_id=1,  # Assuming the first user is valid
            endpoint="https://example.com/endpoint",
            auth="auth-token",
            p256dh="p256dh-key"
        )

        db.session.add(subscription)
        db.session.commit()

        print("Database setup complete. Categories, products, users, and subscriptions have been added.")

if __name__ == "__main__":
    setup_db()
