"""Database Configuration and Connection"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from models.schemas import Base
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
        
        # Add sample data if tables are empty
        add_sample_data()
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_session() -> Session:
    """Get database session"""
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        session.close()
        raise

def add_sample_data():
    """Add sample Apple products to the database"""
    from models.schemas import ProductDB
    
    session = SessionLocal()
    try:
        # Check if products already exist
        if session.query(ProductDB).count() > 0:
            return
        
        sample_products = [
            ProductDB(
                name="iPhone 15 Pro",
                description="The most advanced iPhone ever with titanium design and A17 Pro chip.",
                price=999.99,
                category="iPhone",
                stock=50,
                image_url="https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400"
            ),
            ProductDB(
                name="MacBook Air M2",
                description="Supercharged by M2 chip. Incredibly thin and light design.",
                price=1199.99,
                category="Mac",
                stock=30,
                image_url="https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400"
            ),
            ProductDB(
                name="iPad Pro 12.9\"",
                description="The ultimate iPad experience with M2 chip and Liquid Retina XDR display.",
                price=1099.99,
                category="iPad",
                stock=25,
                image_url="https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400"
            ),
            ProductDB(
                name="Apple Watch Series 9",
                description="Your essential companion for a healthy life with advanced health features.",
                price=399.99,
                category="Watch",
                stock=40,
                image_url="https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400"
            ),
            ProductDB(
                name="AirPods Pro (2nd gen)",
                description="Adaptive Audio. Personalized Spatial Audio. Next-level Active Noise Cancellation.",
                price=249.99,
                category="AirPods",
                stock=60,
                image_url="https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400"
            ),
            ProductDB(
                name="Magic Keyboard",
                description="Wireless, rechargeable keyboard with numeric keypad for Mac.",
                price=199.99,
                category="Accessories",
                stock=35,
                image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400"
            ),
            ProductDB(
                name="iPhone 15",
                description="Dynamic Island. 48MP Main camera. USB-C connectivity.",
                price=799.99,
                category="iPhone",
                stock=45,
                image_url="https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400"
            ),
            ProductDB(
                name="iMac 24\"",
                description="Strikingly thin design powered by M3 chip in vibrant colors.",
                price=1299.99,
                category="Mac",
                stock=20,
                image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400"
            )
        ]
        
        session.add_all(sample_products)
        session.commit()
        logger.info("Sample data added successfully")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding sample data: {e}")
    finally:
        session.close()