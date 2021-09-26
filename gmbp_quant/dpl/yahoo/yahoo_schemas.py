from sqlalchemy import Column, Date, DateTime, BigInteger, Float, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class YahooIpoSchema(Base):
    """Yahoo IPO schema
    """
    __tablename__ = 'yahoo_ipo_stg'
    Symbol = Column(String(100), primary_key=True, nullable=True, default='')
    Company = Column(String(100), primary_key=True, nullable=True, default='')
    Exchange = Column(String(100))
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    IpoDate = Column(DateTime)
    Currency = Column(String(100))
    Price = Column(String(100))
    Shares = Column(String(100))
    Actions = Column(String(100))

    PriceRange = Column(String(100))


class YahooMajorHolderSchema(Base):
    """Yahoo Major Holder schema
    """
    __tablename__ = 'yahoo_major_holders_stg'
    DownloadYearQuarter = Column(String(100), primary_key=True, nullable=False, default='')
    Symbol = Column(String(100), primary_key=True, nullable=False, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    Numbers = Column(String(100), nullable=True, default='')
    HolderCategory = Column(String(200), nullable=True, default='')


class YahooDirectHolderSchema(Base):
    """Yahoo Direct Holder schema
    """
    __tablename__ = 'yahoo_direct_holders_stg'
    DownloadYearQuarter = Column(String(100), primary_key=True, nullable=False, default='')
    Symbol = Column(String(100), primary_key=True, nullable=False, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    Holder = Column(String(100), nullable=True, default='')
    DateReported = Column(Date)
    PercentOut = Column(String(100))
    Shares = Column(Float)
    Value = Column(Float)


class YahooInstitutionHolderSchema(Base):
    """Yahoo Institution Holder schema
    """
    __tablename__ = 'yahoo_institution_holders_stg'
    DownloadYearQuarter = Column(String(100), primary_key=True, nullable=False, default='')
    Symbol = Column(String(100), primary_key=True, nullable=False, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    
    Holder = Column(String(100), nullable=True, default='')
    Shares = Column(Float)
    DateReported = Column(Date)
    PercentOut = Column(String(100))
    Value = Column(Float)


class YahooDailyPriceSchema(Base):
    """Yahoo Daily Price schema
    """
    __tablename__ = 'yahoo_daily_price_stg'
    ticker = Column(String(100), primary_key=True, nullable=True, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    report_date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjclose = Column(Float)
    volume = Column(Float)

class YahooStatsSchema(Base):
    """Yahoo Stats schema
    """
    __tablename__ = 'yahoo_stats_stg'
    symbol = Column(String(100), primary_key=True, nullable=True, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    shares_outstanding = Column(String(100))
    shares_float = Column(String(100))
    insider_holding = Column(String(100))
    institution_holding = Column(String(100))