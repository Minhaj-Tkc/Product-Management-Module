from app import app, db  # Import the app and db from your Flask app
from models import Category, Product, User  # Import your models
from werkzeug.security import generate_password_hash

def setup_db():
    with app.app_context():  # Ensure the app context is active
        # Create all tables in the database
        db.create_all()

        # Add categories
        flowers = Category(category_Name="Flowers", category_description="A variety of beautiful flowers.")
        vegetables = Category(category_Name="Vegetables", category_description="Fresh and organic vegetables.")
        herbs = Category(category_Name="Herbs", category_description="Aromatic and medicinal herbs.")

        db.session.add_all([flowers, vegetables, herbs])
        db.session.commit()

        # Dummy products to populate the database
        dummy_products = [
            Product(
                name="Rose Plant",
                description="A beautiful red rose plant.",
                cost_price=15,
                sell_price=20,
                category_id=flowers.category_id,
                stock_quantity=50,
                image_url="https://bouqs.com/blog/wp-content/uploads/2018/08/shutterstock_1662182848-min-1080x719.jpg"
            ),
            Product(
                name="Tomato Plant",
                description="Healthy tomato plant for fresh produce.",
                cost_price=10,
                sell_price=12,
                category_id=vegetables.category_id,
                stock_quantity=30,
                image_url="https://t3.ftcdn.net/jpg/02/71/63/24/360_F_271632489_iZexHnP4LtGvDD39QvklpgrgdMeGj7PH.jpg"
            ),
            Product(
                name="Aloe Vera",
                description="Low-maintenance aloe vera plant with medicinal properties.",
                cost_price=8,
                sell_price=11,
                category_id=herbs.category_id,
                stock_quantity=40,
                image_url="https://m.media-amazon.com/images/I/81XWpVvk5AL._AC_UF1000,1000_QL80_.jpg"
            ),
        ]

        db.session.add_all(dummy_products)
        db.session.commit()

        # Add dummy users
        dummy_users = [
            User(
                name="Admin User",
                email="admin@example.com",
                password_hash=generate_password_hash("adminpassword"),
                role="Admin"
            ),
            User(
                name="Courier One",
                email="courier1@example.com",
                password_hash=generate_password_hash("courierpassword"),
                role="Courier",
                phone="1234567890",
                vehicle_info="Motorcycle",
                vehicle_number="AB123CD"
            ),
            User(
                name="Courier Two",
                email="courier2@example.com",
                password_hash=generate_password_hash("courierpassword"),
                role="Courier",
                phone="1234567891",
                vehicle_info="Bicycle",
                vehicle_number="EF456GH"
            ),
            User(
                name="Courier Three",
                email="courier3@example.com",
                password_hash=generate_password_hash("courierpassword"),
                role="Courier",
                phone="1234567892",
                vehicle_info="Scooter",
                vehicle_number="IJ789KL"
            ),
            User(
                name="Courier Four",
                email="courier4@example.com",
                password_hash=generate_password_hash("courierpassword"),
                role="Courier",
                phone="1234567893",
                vehicle_info="Activa",
                vehicle_number="MN012OP"
            ),
            User(
                name="user",
                email="user@gmail.com",
                password_hash=generate_password_hash("010203"),
                role="Customer",
                phone="1234567894",
                address="123 Main Street",
                pincode="560001"
            ),
            User(
                name="Customer Two",
                email="customer2@example.com",
                password_hash=generate_password_hash("customerpassword"),
                role="Customer",
                phone="1234567895",
                address="456 Elm Street",
                pincode="560002"
            ),
        ]

        db.session.add_all(dummy_users)
        db.session.commit()

        print("Database setup complete. Categories, products, and users have been added.")

if __name__ == "__main__":
    setup_db()
