from sqlalchemy import Column, Date, BigInteger, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class PolygonCompanySchema(Base):
    """Polygon Company schema
    """
    __tablename__ = 'polygon_company'
    cik = Column(String(100), primary_key=True, nullable=True, default='')
    symbol = Column(String(100), primary_key=True, nullable=False)

    row_num = Column(BigInteger, primary_key=True, nullable=False)

    active = Column(Boolean)
    bloomberg = Column(String(100))
    ceo = Column(String(100))
    country = Column(String(100))
    employees = Column(String(100))
    exchange = Column(String(100))
    exchangeSymbol = Column(String(100))
    figi = Column(String(100))
    hq_address = Column(String(100))
    hq_country = Column(String(100))
    hq_state = Column(String(100))
    industry = Column(String(100))
    lei = Column(String(100))
    listdate = Column(Date)
    logo = Column(String(100))
    marketcap = Column(Float)
    name = Column(String(500))
    phone = Column(String(100))
    sector = Column(String(100))
    sic = Column(String(100))
    type = Column(String(100))
    updated = Column(String(100))
    url = Column(String(100))
