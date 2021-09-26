from sqlalchemy import Column, Date, DateTime, BigInteger, Float, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class TiingoDailyPriceSchema(Base):
    """Tiingo Daily Price schema
    """
    __tablename__ = 'tiingo_daily_price'
    symbol = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(DateTime, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    closePrice = Column(Float)
    high = Column(Float)
    low = Column(Float)
    openPrice = Column(Float)
    volume = Column(Float)
    adjClose = Column(Float)
    adjHigh = Column(Float)
    adjLow = Column(Float)
    adjOpen = Column(Float)
    adjVolume = Column(Float)
    divCash = Column(Float)
    splitFactor = Column(Float)
