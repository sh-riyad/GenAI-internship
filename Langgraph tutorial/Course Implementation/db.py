from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from schemas import StoreProductInput, StoreServiceInput

Base = declarative_base()

engine = create_engine('sqlite:///amar-shop.db', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    product_code = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    expiry_date = Column(Date, nullable=False)
    brand = Column(String, nullable=False)
    product_type = Column(String, nullable=False)

    def __repr__(self):
        return f"<Product(name='{self.name}', product_code='{self.product_code}', price={self.price}, expiry_date='{self.expiry_date}', brand='{self.brand}', product_type='{self.product_type}')>"


class Services(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    service_code = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Product(name='{self.name}', product_code='{self.product_code}', price={self.price}, available_quantity={self.available_quantity}, expiry_date='{self.expiry_date}', brand='{self.brand}', product_type='{self.product_type}')>"


Base.metadata.create_all(engine)


def store_products(input_data: StoreProductInput, db: Session):
    """
    Inserts a product into the groceries_product table in the database.
    """
    db_product = Products(
        name=input_data.name,
        product_code=input_data.product_code,
        price=input_data.price,
        expiry_date=input_data.expiry_date,
        brand=input_data.brand,
        product_type=input_data.product_type
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def store_service(input_data: StoreServiceInput, db: Session):
    """
    Inserts a new service into the 'services' table.
    """
    # Create a new Service instance
    new_service = Services(
        name=input_data.name,
        service_code=input_data.service_code,
        price=input_data.price
    )

    # Add the new service to the session
    db.add(new_service)
    db.commit()  # Commit the transaction
    db.refresh(new_service)  # Refresh to get the updated object

    return new_service



sample_products = [
    StoreProductInput(name="Miniket Rice", product_code="MR001", price=74.0, expiry_date="2025-12-31", brand="Aarong", product_type="Rice"),
    StoreProductInput(name="Chinigura Rice", product_code="CR002", price=115.0, expiry_date="2025-11-30", brand="Kazi Farms", product_type="Rice"),
    StoreProductInput(name="Soyabean Oil", product_code="SO003", price=177.0, expiry_date="2026-06-15", brand="Sundarban", product_type="Oil"),
    StoreProductInput(name="White Sugar", product_code="WS004", price=128.0, expiry_date="2026-01-20", brand="S. A. Group", product_type="Sugar"),
    StoreProductInput(name="Red Lentil (Masoor Dal)", product_code="RL005", price=119.0, expiry_date="2025-09-10", brand="PRAN", product_type="Lentil"),
    StoreProductInput(name="Mustard Oil", product_code="MO006", price=150.0, expiry_date="2026-05-10", brand="Rupchanda", product_type="Oil"),
    StoreProductInput(name="Green Chili", product_code="GC007", price=40.0, expiry_date="2025-09-15", brand="FreshMart", product_type="Vegetable"),
    StoreProductInput(name="Potato", product_code="PT008", price=30.0, expiry_date="2025-12-20", brand="FarmFresh", product_type="Vegetable"),
    StoreProductInput(name="Onion", product_code="ON009", price=50.0, expiry_date="2025-11-25", brand="DeshiOnion", product_type="Vegetable"),
    StoreProductInput(name="Garlic", product_code="GL010", price=60.0, expiry_date="2025-10-30", brand="PureSpice", product_type="Spice"),
    StoreProductInput(name="Ginger", product_code="GN011", price=70.0, expiry_date="2025-09-05", brand="SpiceKing", product_type="Spice"),
    StoreProductInput(name="Turmeric Powder", product_code="TP012", price=80.0, expiry_date="2026-01-15", brand="GoldenSpice", product_type="Spice"),
    StoreProductInput(name="Coriander Powder", product_code="CP013", price=90.0, expiry_date="2026-02-10", brand="GreenLeaf", product_type="Spice"),
    StoreProductInput(name="Cumin Seeds", product_code="CS014", price=110.0, expiry_date="2026-03-05", brand="RoyalSpice", product_type="Spice"),
    StoreProductInput(name="Fennel Seeds", product_code="FS015", price=120.0, expiry_date="2026-04-01", brand="TasteBuds", product_type="Spice")
]

sample_services = [
    StoreServiceInput(name="Car Wash", service_code="CW001", price=20.0),
    StoreServiceInput(name="House Cleaning", service_code="HC002", price=35.0),
    StoreServiceInput(name="Lawn Mowing", service_code="LM003", price=40.0),
    StoreServiceInput(name="Plumbing Service", service_code="PS004", price=60.0),
    StoreServiceInput(name="Electrical Service", service_code="ES005", price=75.0),
    StoreServiceInput(name="Pest Control", service_code="PC006", price=50.0),
    StoreServiceInput(name="Handyman Service", service_code="HS007", price=45.0),
    StoreServiceInput(name="Window Cleaning", service_code="WC008", price=30.0),
    StoreServiceInput(name="Laundry Service", service_code="LS009", price=15.0),
    StoreServiceInput(name="Carpet Cleaning", service_code="CC010", price=25.0),
    StoreServiceInput(name="Deep Cleaning", service_code="DC011", price=55.0),
    StoreServiceInput(name="Appliance Repair", service_code="AR012", price=70.0),
    StoreServiceInput(name="Gutter Cleaning", service_code="GC013", price=40.0),
    StoreServiceInput(name="Moving Services", service_code="MS014", price=100.0)
]


database = SessionLocal()

for product in sample_products:
    store_products(product, database)

for service in sample_services:
    store_service(service, database)


# class GetProductInput(BaseModel):
#     product_type: str
#     skip: int = 0
#     limit: int = 10
#
#     class Config:
#         from_attributes = True
#
#
# def get_products_by_type(input_data: GetProductInput, db: Session):
#     """
#     Fetches all products from the 'products' table that match the given product type.
#     """
#     return db.query(Products).filter(Products.product_type == input_data.product_type).offset(input_data.skip).limit(
#         input_data.limit).all()
#
#
# db = SessionLocal()
# rice_products = get_products_by_type(GetProductInput(product_type="Rice"), db)
#
# for product in rice_products:
#     print(product)