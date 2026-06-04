import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("FATAL: DATABASE_URL environment variable is missing.")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- THE POSTGRES TABLE SCHEMA ---
class DBMarketTick(Base):
    __tablename__ = 'market_ticks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False)
    trade_date = Column(Date, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

def save_ticks_to_db(validated_ticks):
    """Takes a list of Pydantic MarketTick objects and saves them to Postgres."""
    
    # CRITICAL FIX: Defer table creation until this function is explicitly called.
    # This prevents the script from crashing during the 'import' phase if the DB is down.
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        raise Exception(f"Database network unreachable: {e}")

    session = SessionLocal()
    try:
        db_records = [
            DBMarketTick(
                symbol=tick.symbol,
                trade_date=tick.trade_date,
                open_price=tick.open_price,
                high_price=tick.high_price,
                low_price=tick.low_price,
                close_price=tick.close_price,
                volume=tick.volume
            ) for tick in validated_ticks
        ]
        
        session.add_all(db_records)
        session.commit()
        return True
        
    except Exception as e:
        session.rollback()
        raise Exception(f"Database Insertion Failed: {e}")
    finally:
        session.close()