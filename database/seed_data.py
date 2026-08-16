"""Seed script to populate database with test data."""

from database.db import get_db_session, init_db
from database.models import (
    Category, Subcategory, Product, ProductType, ProductKey, User
)
from datetime import datetime


def seed_test_data():
    """Populate database with realistic test data."""
    print("Seeding test data...")
    
    with get_db_session() as session:
        # Create test admin user
        admin_user = session.query(User).filter_by(telegram_id=6505578903).first()
        if not admin_user:
            admin_user = User(
                telegram_id=6505578903,
                username="novainintelligence-tech",
                wallet_balance=0.0
            )
            session.add(admin_user)
            print("✓ Admin user created")

        # CATEGORY 1: PREMIUM SOFTWARE
        cat1 = session.query(Category).filter_by(name="Premium Software").first()
        if not cat1:
            cat1 = Category(
                name="Premium Software",
                description="High-quality software licenses and tools"
            )
            session.add(cat1)
            session.flush()
            print("✓ Category: Premium Software")

            # Subcategories
            subcat1_1 = Subcategory(
                name="Productivity Tools",
                category_id=cat1.id
            )
            subcat1_2 = Subcategory(
                name="Design Software",
                category_id=cat1.id
            )
            session.add_all([subcat1_1, subcat1_2])
            session.flush()

            # Products in Productivity
            prod1_1 = Product(
                name="Microsoft Office Professional 2024",
                description="Complete office suite with Word, Excel, PowerPoint",
                price=99.99,
                category_id=cat1.id,
                subcategory_id=subcat1_1.id,
                product_type=ProductType.KEY,
                stock_count=50
            )
            prod1_2 = Product(
                name="Notion Premium Annual",
                description="All-in-one workspace, valid for 12 months",
                price=99.00,
                category_id=cat1.id,
                subcategory_id=subcat1_1.id,
                product_type=ProductType.KEY,
                stock_count=75
            )
            session.add_all([prod1_1, prod1_2])
            session.flush()

            # Add keys for Microsoft Office
            for i in range(10):
                key = ProductKey(
                    product_id=prod1_1.id,
                    key_value=f"PROD-KEY-{prod1_1.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            # Add keys for Notion
            for i in range(15):
                key = ProductKey(
                    product_id=prod1_2.id,
                    key_value=f"NOTION-PRO-{prod1_2.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            # Products in Design
            prod1_3 = Product(
                name="Adobe Creative Cloud 2024",
                description="Photoshop, Illustrator, InDesign, Premiere - 1 year",
                price=599.99,
                category_id=cat1.id,
                subcategory_id=subcat1_2.id,
                product_type=ProductType.KEY,
                stock_count=30
            )
            prod1_4 = Product(
                name="Figma Professional",
                description="Design collaboration platform premium license",
                price=144.00,
                category_id=cat1.id,
                subcategory_id=subcat1_2.id,
                product_type=ProductType.KEY,
                stock_count=60
            )
            session.add_all([prod1_3, prod1_4])
            session.flush()

            # Add keys for Adobe
            for i in range(8):
                key = ProductKey(
                    product_id=prod1_3.id,
                    key_value=f"ADOBE-CC-{prod1_3.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            # Add keys for Figma
            for i in range(12):
                key = ProductKey(
                    product_id=prod1_4.id,
                    key_value=f"FIGMA-PRO-{prod1_4.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            print("✓ Subcategories and products added (Premium Software)")

        # CATEGORY 2: DEVELOPMENT TOOLS
        cat2 = session.query(Category).filter_by(name="Development Tools").first()
        if not cat2:
            cat2 = Category(
                name="Development Tools",
                description="Tools and IDE for software developers"
            )
            session.add(cat2)
            session.flush()
            print("✓ Category: Development Tools")

            subcat2_1 = Subcategory(
                name="IDEs & Editors",
                category_id=cat2.id
            )
            subcat2_2 = Subcategory(
                name="DevOps & Hosting",
                category_id=cat2.id
            )
            session.add_all([subcat2_1, subcat2_2])
            session.flush()

            # Products in IDEs
            prod2_1 = Product(
                name="JetBrains IntelliJ IDEA Ultimate",
                description="Advanced IDE for Java, Kotlin, Python, and more",
                price=199.00,
                category_id=cat2.id,
                subcategory_id=subcat2_1.id,
                product_type=ProductType.KEY,
                stock_count=45
            )
            prod2_2 = Product(
                name="Visual Studio Professional",
                description="Complete IDE for .NET development",
                price=249.99,
                category_id=cat2.id,
                subcategory_id=subcat2_1.id,
                product_type=ProductType.KEY,
                stock_count=40
            )
            session.add_all([prod2_1, prod2_2])
            session.flush()

            # Add keys
            for i in range(10):
                key = ProductKey(
                    product_id=prod2_1.id,
                    key_value=f"INTELLIJ-{prod2_1.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            for i in range(10):
                key = ProductKey(
                    product_id=prod2_2.id,
                    key_value=f"VSPRO-{prod2_2.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            # Products in DevOps
            prod2_3 = Product(
                name="AWS Premium Support",
                description="1 month AWS Premium Support subscription",
                price=100.00,
                category_id=cat2.id,
                subcategory_id=subcat2_2.id,
                product_type=ProductType.KEY,
                stock_count=20
            )
            prod2_4 = Product(
                name="DigitalOcean App Platform Credit",
                description="$100 credit for DigitalOcean services",
                price=100.00,
                category_id=cat2.id,
                subcategory_id=subcat2_2.id,
                product_type=ProductType.KEY,
                stock_count=50
            )
            session.add_all([prod2_3, prod2_4])
            session.flush()

            for i in range(5):
                key = ProductKey(
                    product_id=prod2_3.id,
                    key_value=f"AWS-SUPPORT-{prod2_3.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            for i in range(10):
                key = ProductKey(
                    product_id=prod2_4.id,
                    key_value=f"DIGITALOCEAN-{prod2_4.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            print("✓ Subcategories and products added (Development Tools)")

        # CATEGORY 3: SECURITY & PRIVACY
        cat3 = session.query(Category).filter_by(name="Security & Privacy").first()
        if not cat3:
            cat3 = Category(
                name="Security & Privacy",
                description="VPN, antivirus, and security solutions"
            )
            session.add(cat3)
            session.flush()
            print("✓ Category: Security & Privacy")

            subcat3_1 = Subcategory(
                name="VPN Services",
                category_id=cat3.id
            )
            subcat3_2 = Subcategory(
                name="Antivirus & Protection",
                category_id=cat3.id
            )
            session.add_all([subcat3_1, subcat3_2])
            session.flush()

            # VPN Products
            prod3_1 = Product(
                name="NordVPN Premium 1 Year",
                description="VPN protection for 1 year, all devices",
                price=89.99,
                category_id=cat3.id,
                subcategory_id=subcat3_1.id,
                product_type=ProductType.KEY,
                stock_count=100
            )
            prod3_2 = Product(
                name="ExpressVPN 1 Year",
                description="Fast VPN service, 1 year subscription",
                price=99.95,
                category_id=cat3.id,
                subcategory_id=subcat3_1.id,
                product_type=ProductType.KEY,
                stock_count=80
            )
            session.add_all([prod3_1, prod3_2])
            session.flush()

            for i in range(20):
                key = ProductKey(
                    product_id=prod3_1.id,
                    key_value=f"NORDVPN-{prod3_1.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            for i in range(15):
                key = ProductKey(
                    product_id=prod3_2.id,
                    key_value=f"EXPRESSVPN-{prod3_2.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            # Antivirus Products
            prod3_3 = Product(
                name="Kaspersky Premium 1 Year",
                description="Complete antivirus protection for 1 year",
                price=49.99,
                category_id=cat3.id,
                subcategory_id=subcat3_2.id,
                product_type=ProductType.KEY,
                stock_count=70
            )
            prod3_4 = Product(
                name="McAfee Total Protection",
                description="Comprehensive protection suite, 1 year",
                price=39.99,
                category_id=cat3.id,
                subcategory_id=subcat3_2.id,
                product_type=ProductType.KEY,
                stock_count=90
            )
            session.add_all([prod3_3, prod3_4])
            session.flush()

            for i in range(14):
                key = ProductKey(
                    product_id=prod3_3.id,
                    key_value=f"KASPERSKY-{prod3_3.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            for i in range(18):
                key = ProductKey(
                    product_id=prod3_4.id,
                    key_value=f"MCAFEE-{prod3_4.id}-{i+1:04d}",
                    is_sold=False
                )
                session.add(key)

            print("✓ Subcategories and products added (Security & Privacy)")

        session.commit()

    print("[OK] Database seeded with test data successfully!")


if __name__ == "__main__":
    init_db()
    seed_test_data()
