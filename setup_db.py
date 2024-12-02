from app import app, db, Product  # Import the app and database

def setup_database():
    # Create tables and add dummy data
    with app.app_context():  # Use the app context from `app`
        db.create_all()

        # Dummy products to populate the database
        dummy_products = [
            Product(
                name="Rose Plant",
                description="A beautiful red rose plant.",
                price=10.99,
                weight=1.2,
                category="Flowers",
                stock=50,  # Added stock
                image_url="https://bouqs.com/blog/wp-content/uploads/2018/08/shutterstock_1662182848-min-1080x719.jpg"  # Dummy image URL
            ),
            Product(
                name="Basil Seeds",
                description="Organic basil seeds for your garden.",
                price=2.49,
                weight=0.05,
                category="Herbs",
                stock=100,  # Added stock
                image_url="https://static.toiimg.com/thumb/msid-112426676,width-1070,height-580,imgsize-73742,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg"  # Dummy image URL
            ),
            Product(
                name="Tomato Plant",
                description="Healthy tomato plant for fresh produce.",
                price=8.99,
                weight=1.5,
                category="Vegetables",
                stock=30,  # Added stock
                image_url="https://t3.ftcdn.net/jpg/02/71/63/24/360_F_271632489_iZexHnP4LtGvDD39QvklpgrgdMeGj7PH.jpg"  # Dummy image URL
            ),
        ]

        # Add products if none exist
        if not Product.query.first():
            db.session.add_all(dummy_products)
            db.session.commit()
            print("Dummy products added successfully!")
        else:
            print("Products already exist. No changes made.")

if __name__ == "__main__":
    setup_database()
