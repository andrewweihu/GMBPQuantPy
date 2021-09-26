"""
Those Schema's are used to construct database.

Every Schema must have: __tablename__, cik, document_id, row_num

The link "https://sec.report/Document/{document_id}/" will take you to the document.
Example: https://sec.report/Document/0000746210-20-000056/
"""

from sqlalchemy import Column, Date, BigInteger, Float, String, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sec13FHRSchema(Base):
    """SEC form 13F-HR schema
    """
    __tablename__ = 'sec_13fhr'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(200))
    title_of_class = Column(String(100))
    cusip = Column(String(100))
    values = Column(BigInteger)
    ssh_prn_amt = Column(BigInteger)
    ssh_prn_type = Column(String(50))
    put_call = Column(String(100))
    other_manager = Column(String(100))
    investment_discretion = Column(String(50))
    voting_authority_sole = Column(BigInteger)
    voting_authority_shared = Column(BigInteger)
    voting_authority_none = Column(BigInteger)


class Sec13FHRASchema(Base):
    """SEC form 13F-HRA schema
    """
    __tablename__ = 'sec_13fhra'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    amendment_num = Column(BigInteger)
    amendment_type = Column(String(100))
    name = Column(String(200))
    title_of_class = Column(String(100))
    cusip = Column(String(100))
    values = Column(BigInteger)
    ssh_prn_amt = Column(BigInteger)
    ssh_prn_type = Column(String(50))
    put_call = Column(String(100))
    other_manager = Column(String(100))
    investment_discretion = Column(String(50))
    voting_authority_sole = Column(BigInteger)
    voting_authority_shared = Column(BigInteger)
    voting_authority_none = Column(BigInteger)


class Sec4NonDerivativeSchema(Base):
    """SEC form 4 Non-Derivative schema
    """
    __tablename__ = 'sec_4_nonderivative'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(50))
    security_title = Column(String(200))
    transaction_date = Column(Date)
    deemed_execution_date = Column(Date)
    transaction_coding_form_type = Column(String(50))
    transaction_coding_code = Column(String(50))
    transaction_coding_equity_swap_involved = Column(Float)
    transaction_shares = Column(Float)
    transaction_price_per_share = Column(Float)
    transaction_acquired_disposed_code = Column(String(50))
    shares_owned_following_transaction = Column(Float)
    direct_or_indirect_ownership = Column(String(50))
    nature_of_ownership = Column(String(500))


class Sec4DerivativeSchema(Base):
    """SEC form 4 Derivative schema
    """
    __tablename__ = 'sec_4_derivative'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(50))
    security_title = Column(String(200))
    conversion_or_exercise_price = Column(Float)
    transaction_date = Column(Date)
    deemed_execution_date = Column(Date)
    transaction_coding_form_type = Column(String(50))
    transaction_coding_code = Column(String(50))
    transaction_coding_equity_swap_involved = Column(Float)
    transaction_shares = Column(Float)
    transaction_price_per_share = Column(Float)
    transaction_acquired_disposed_code = Column(String(50))
    shares_owned_following_transaction = Column(Float)
    exercise_date = Column(Date)
    expiration_date = Column(Date)
    underlying_security_title = Column(String(200))
    underlying_security_shares = Column(Float)
    direct_or_indirect_ownership = Column(String(50))
    nature_of_ownership = Column(String(500))


class Sec4ReportingOwnerSchema(Base):
    """SEC form 4 reporting owner schema
    """
    __tablename__ = 'sec_4_reportingowner'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(50))
    report_owner_cik = Column(String(100))
    report_owner_name = Column(String(100))
    street1 = Column(String(50))
    street2 = Column(String(50))
    city = Column(String(40))
    state = Column(String(2))
    zipcode = Column(String(15))
    state_description = Column(String(50))
    is_director = Column(BOOLEAN)
    is_officer = Column(BOOLEAN)
    is_ten_percent_owner = Column(BOOLEAN)
    is_other = Column(BOOLEAN)
    officer_title = Column(String(40))
    other_text = Column(String(50))


class Sec3NonDerivativeSchema(Base):
    """SEC form 3 Non-Derivative schema
    """
    __tablename__ = 'sec_3_nonderivative'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(50))
    security_title = Column(String(200))
    shares_owned_following_transaction = Column(Float)
    direct_or_indirect_ownership = Column(String(50))
    nature_of_ownership = Column(String(500))


class Sec3DerivativeSchema(Base):
    """SEC form 3 Derivative schema
    """
    __tablename__ = 'sec_3_derivative'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(50))
    security_title = Column(String(200))
    conversion_or_exercise_price = Column(Float)
    exercise_date = Column(Date)
    expiration_date = Column(Date)
    underlying_security_title = Column(String(200))
    underlying_security_shares = Column(Float)
    direct_or_indirect_ownership = Column(String(50))
    nature_of_ownership = Column(String(500))


class Sec3ReportingOwnerSchema(Base):
    """SEC form 3 reporting owner schema
    """
    __tablename__ = 'sec_3_reportingowner'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(50))
    report_owner_cik = Column(String(100))
    report_owner_name = Column(String(100))
    street1 = Column(String(50))
    street2 = Column(String(50))
    city = Column(String(40))
    state = Column(String(2))
    zipcode = Column(String(15))
    state_description = Column(String(50))
    is_director = Column(BOOLEAN)
    is_officer = Column(BOOLEAN)
    is_ten_percent_owner = Column(BOOLEAN)
    is_other = Column(BOOLEAN)
    officer_title = Column(String(40))
    other_text = Column(String(50))


class SecS3Schema(Base):
    """
    SEC Form S-3 is a regulatory filing that provides simplified reporting
    for issuers of registered securities.
    """
    __tablename__ = 'sec_s3'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    date_as_of_change = Column(Date, primary_key=True, nullable=False)
    company_conformed_name = Column(String(100))
    title_of_each_class = Column(String(100))
    amount_of_each_class = Column(String(100))  # might contain words, comma, $ sign, etc
    max_offering_price = Column(String(100))
    max_aggregate_price = Column(String(100))
    registration_fee = Column(String(100))


class SecS1Schema(Base):
    """
    SEC Form S-1 is a regulatory filing that provides reporting
    for issuers of registered securities.
    """
    __tablename__ = 'sec_s1'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    filed_as_of_date = Column(Date, primary_key=True, nullable=False)
    company_conformed_name = Column(String(100))
    title_of_each_class = Column(String(100))
    amount_of_each_class = Column(String(100))  # might contain words, comma, $ sign, etc
    max_offering_price = Column(String(100))
    max_aggregate_price = Column(String(100))
    registration_fee = Column(String(100))


class Sec144Schema(Base):
    """
    SEC Form 144 is a form filed with the SEC by an executive officer, director,
    or the affiliate of a company when placing an order to sell that company's stock
    during any three-month period in which the sale exceeds 5,000 shares or units
    or has an aggregate sales price greater than $50,000.
    """
    __tablename__ = 'sec_144'
    cik = Column(String(100), primary_key=True, nullable=False)
    document_id = Column(String(100), primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    filed_as_of_date = Column(Date, primary_key=True, nullable=False)
    company_conformed_name = Column(String(100))
    