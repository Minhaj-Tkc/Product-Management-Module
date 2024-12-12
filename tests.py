import unittest
from app import app, db
from models import User, Product, Category
from flask_login import login_user

class TestRoutes(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            # Create a test user
            self.user = User(
                name="Test Gardener",
                email="gardener@example.com",
                role="Customer",
                address="123 Garden Lane",
                phone="9876543210",
                pincode="456789"
            )
            self.user.set_password("password")
            db.session.add(self.user)

            # Create garden-related categories
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

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_show_products(self):
        with app.app_context():
            # user instance to the active session
            self.user = db.session.merge(self.user)

            # Simulate user login by setting the session
            with self.client.session_transaction() as session:
                session["_user_id"] = str(self.user.id)

            # Send GET request to the /show_products route
            response = self.client.get("/show_products")
            self.assertEqual(response.status_code, 200)  # Check for successful response
            self.assertIn(b"Rose Plant", response.data)  # Check if Rose Plant appears in the response
            self.assertIn(b"Tomato Plant", response.data)  # Check if Tomato Plant appears in the response
            self.assertIn(b"Aloe Vera", response.data)  # Check if Aloe Vera appears in the response


if __name__ == "__main__":
    unittest.main()
