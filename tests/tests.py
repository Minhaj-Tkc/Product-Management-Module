import unittest
from app import app, db, User, Product
from flask_login import login_user

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        # Initialize the database
        with app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        """Clean up the test database."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Create sample data for testing."""
        # Create a test user
        user = User(email='test@example.com', password='password', role='Customer')
        user.set_password('password')  # Assuming you have a password hashing method
        db.session.add(user)

        # Create a sample product
        product = Product(name='Test Product', sell_price=10.0)
        db.session.add(product)
        db.session.commit()

    def login(self, email, password):
        """Helper method to log in a test user."""
        return self.client.post('/', data=dict(email=email, password=password), follow_redirects=True)

    def test_login_page_loads(self):
        """Test that the login page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_success(self):
        """Test a successful login."""
        response = self.login('test@example.com', 'password')
        self.assertIn(b'Login successful!', response.data)

    def test_login_failure(self):
        """Test an unsuccessful login."""
        response = self.login('wrong@example.com', 'wrongpassword')
        self.assertIn(b'Invalid email or password', response.data)

    def test_products_page(self):
        """Test that the products page loads and displays products."""
        with self.client:
            self.login('test@example.com', 'password')  # Simulate login
            response = self.client.get('/products')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Product', response.data)

    def test_add_to_cart(self):
        """Test adding a product to the cart."""
        with self.client:
            self.login('test@example.com', 'password')
            product = Product.query.first()
            response = self.client.post(f'/add_to_cart/{product.id}', follow_redirects=True)
            self.assertIn(b'added to cart', response.data)

    def test_view_cart(self):
        """Test viewing the cart."""
        with self.client:
            self.login('test@example.com', 'password')
            response = self.client.get('/cart')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your cart', response.data)  # Update with actual text in your cart page

if __name__ == '__main__':
    unittest.main()
