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
                stock=50,
                image_url="https://bouqs.com/blog/wp-content/uploads/2018/08/shutterstock_1662182848-min-1080x719.jpg"
            ),
            Product(
                name="Tomato Plant",
                description="Healthy tomato plant for fresh produce.",
                price=8.99,
                weight=1.5,
                category="Vegetables",
                stock=30,
                image_url="https://t3.ftcdn.net/jpg/02/71/63/24/360_F_271632489_iZexHnP4LtGvDD39QvklpgrgdMeGj7PH.jpg"
            ),
            Product(
                name="Aloe Vera",
                description="Low-maintenance aloe vera plant with medicinal properties.",
                price=6.99,
                weight=0.8,
                category="Succulents",
                stock=40,
                image_url="https://m.media-amazon.com/images/I/81XWpVvk5AL._AC_UF1000,1000_QL80_.jpg"
            ),
            Product(
                name="Basil Seeds",
                description="Organic basil seeds for your garden.",
                price=2.49,
                weight=0.05,
                category="Herbs",
                stock=100,
                image_url="https://i.ytimg.com/vi/F89GdaWJi14/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBKDGbGm-aWqzdiCXJCbqX75J4jsQ"
            ),
            Product(
                name="Sunflower Seeds",
                description="Pack of sunflower seeds for gardening.",
                price=3.49,
                weight=0.1,
                category="Seeds",
                stock=150,
                image_url="https://static.toiimg.com/thumb/msid-106160081,width-1280,height-720,resizemode-4/106160081.jpg"
            ),
            Product(
                name="Orchid Plant",
                description="Elegant orchid plant perfect for home decor.",
                price=25.99,
                weight=1.0,
                category="Flowers",
                stock=20,
                image_url="https://rukminim2.flixcart.com/image/850/1000/xif0q/plant-sapling/j/y/u/yes-perennial-yes-orchid-flower-plant-air-purifier-plant-fmn3612-original-imagpj64thsjmsdc.jpeg?q=20&crop=false"
            ),
            Product(
                name="Mint Plant",
                description="Fresh mint plant for culinary uses.",
                price=4.99,
                weight=0.5,
                category="Herbs",
                stock=60,
                image_url="https://www.geturbanleaf.com/cdn/shop/articles/1008bcba2907fadf07e2f5986a9aab49.jpg?v=1704822162"
            ),
            Product(
                name="Basil Seeds",
                description="Organic basil seeds for your garden.",
                price=2.49,
                weight=0.05,
                category="Herbs",
                stock=100,
                image_url="https://i.ytimg.com/vi/F89GdaWJi14/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBKDGbGm-aWqzdiCXJCbqX75J4jsQ"
            )
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
