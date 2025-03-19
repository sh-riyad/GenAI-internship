from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from schemas import StoreProductInput, StoreServiceInput

Base = declarative_base()

engine = create_engine('sqlite:///career-assistant.db', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Resources(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=True)
    file =

    def __repr__(self):
        return f"<Product(name='{self.name}', product_code='{self.product_code}', price={self.price}, expiry_date='{self.expiry_date}', brand='{self.brand}', product_type='{self.product_type}')>"


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

database = SessionLocal()
