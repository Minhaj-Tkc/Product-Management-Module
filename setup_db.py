from app import app, db  # Import the app and db from your Flask app
from models import Category, Product  # Import your models

def setup_db():
    with app.app_context():  # Ensure the app context is active
        # Create all tables in the database
        db.create_all()

        # Add categories
        flowers = Category(category_Name="Flowers", Category_description="A variety of beautiful flowers.")
        vegetables = Category(category_Name="Vegetables", Category_description="Fresh and organic vegetables.")
        herbs = Category(category_Name="Herbs", Category_description="Aromatic and medicinal herbs.")

        db.session.add_all([flowers, vegetables, herbs])
        db.session.commit()

        # Dummy products to populate the database
        dummy_products = [
            Product(
                name="Rose Plant",
                description="A beautiful red rose plant.",
                price=10.99,
                category_id=flowers.category_id,
                stock_quantity=50,
                image_url="https://bouqs.com/blog/wp-content/uploads/2018/08/shutterstock_1662182848-min-1080x719.jpg"
            ),
            Product(
                name="Tomato Plant",
                description="Healthy tomato plant for fresh produce.",
                price=8.99,
                category_id=flowers.category_id,
                stock_quantity=30,
                image_url="https://t3.ftcdn.net/jpg/02/71/63/24/360_F_271632489_iZexHnP4LtGvDD39QvklpgrgdMeGj7PH.jpg"
            ),
            Product(
                name="Aloe Vera",
                description="Low-maintenance aloe vera plant with medicinal properties.",
                price=6.99,
                category_id=herbs.category_id,
                stock_quantity=40,
                image_url="https://m.media-amazon.com/images/I/81XWpVvk5AL._AC_UF1000,1000_QL80_.jpg"
            ),
            Product(
                name="Basil Seeds",
                description="Organic basil seeds for your garden.",
                price=2.49,
                category_id=herbs.category_id,
                stock_quantity=100,
                image_url="https://i.ytimg.com/vi/F89GdaWJi14/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBKDGbGm-aWqzdiCXJCbqX75J4jsQ"
            ),
            Product(
                name="Sunflower Seeds",
                description="Pack of sunflower seeds for gardening.",
                price=3.49,
                category_id=flowers.category_id,
                stock_quantity=150,
                image_url="https://static.toiimg.com/thumb/msid-106160081,width-1280,height-720,resizemode-4/106160081.jpg"
            ),
            Product(
                name="Orchid Plant",
                description="Elegant orchid plant perfect for home decor.",
                price=25.99,
                category_id=flowers.category_id,
                stock_quantity=20,
                image_url="https://rukminim2.flixcart.com/image/850/1000/xif0q/plant-sapling/j/y/u/yes-perennial-yes-orchid-flower-plant-air-purifier-plant-fmn3612-original-imagpj64thsjmsdc.jpeg?q=20&crop=false"
            ),
            Product(
                name="Mint Plant",
                description="Fresh mint plant for culinary uses.",
                price=4.99,
                category_id=herbs.category_id,
                stock_quantity=60,
                image_url="https://www.geturbanleaf.com/cdn/shop/articles/1008bcba2907fadf07e2f5986a9aab49.jpg?v=1704822162"
            ),
            Product(
                name="Basil Seeds",
                description="Organic basil seeds for your garden.",
                price=2.49,
                category_id=herbs.category_id,
                stock_quantity=100,
                image_url="https://i.ytimg.com/vi/F89GdaWJi14/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBKDGbGm-aWqzdiCXJCbqX75J4jsQ"
            )
        ]

        db.session.add_all(dummy_products)
        db.session.commit()

        print("Database setup complete. Categories and products have been added.")

if __name__ == "__main__":
    setup_db()





