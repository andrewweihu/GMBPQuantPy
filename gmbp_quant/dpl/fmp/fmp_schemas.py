"""
This file defines schema for database tables under database mktdata.

For each schema, __tablename__ and row_num must be defined,
and they are not from the jason file downloaded from FMP.
"""

from sqlalchemy import Column, Date, Time, BigInteger, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Fmp10QSchema(Base):
    """FMP form 10Q schema
    """
    __tablename__ = 'fmp_10q'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    year = Column(Integer, primary_key=True, nullable=True)
    period = Column(String(2), primary_key=True, nullable=True)
    shares_outstanding = Column(BigInteger)
    cls = Column(Integer)


class Fmp10KSchema(Base):
    """FMP form 10K schema
    """
    __tablename__ = 'fmp_10k'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    year = Column(Integer, primary_key=True, nullable=True)
    shares_outstanding = Column(Float)
    cls = Column(Integer)


class FmpSharesFloatSchema(Base):
    """FMP shares float schema
    """
    __tablename__ = 'fmp_shares_float'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    shares_outstanding = Column(Float)
    float_shares = Column(Float)
    date_reported = Column(Date)


class Fmp13FSchema(Base):
    """FMP form 13F schema
    """
    __tablename__ = 'fmp_13f'
    cik = Column(String(100), primary_key=True, nullable=False)
    cusip = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    fillingDate = Column(Date, primary_key=True, nullable=False)
    acceptedDate = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    nameOfIssuer = Column(String(200))
    titleOfClass = Column(String(100))
    tickercusip = Column(String(100))
    value = Column(BigInteger)
    shares = Column(BigInteger)
    link = Column(String(200))
    finalLink = Column(String(200))


class Fmp4Schema(Base):
    """Fmp form 4 schema
    """
    __tablename__ = 'fmp_4'
    cik = Column(String(100), primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)


class FmpEtfSchema(Base):
    """Fmp ETF schema
    """
    __tablename__ = 'fmp_etf'
    symbol = Column(String(100), primary_key=True, nullable=False)
    name = Column(String(500), primary_key=True, nullable=False)
    exchange = Column(String(100), primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    price = Column(Float)


class FmpCikNameMapSchema(Base):
    """Fmp Cik Name schema
    """
    __tablename__ = 'fmp_cik_name'
    reportingCik = Column(String(100), primary_key=True, nullable=False)
    reportingName = Column(String(500), primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)


class FmpSecCikNameMapSchema(Base):
    """Fmp Sec Cik Name schema
    """
    __tablename__ = 'fmp_sec_cik_name'
    cik = Column(String(100), primary_key=True, nullable=True, default='')
    company_name = Column(String(500), primary_key=True, nullable=True, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)


class FmpInstHolderSchema(Base):
    """Fmp Institutional Holder schema
    """
    __tablename__ = 'fmp_inst_holder'
    ticker = Column(String(100), primary_key=True, nullable=False)
    holder = Column(String(100), primary_key=True, nullable=False)
    dateReported = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    shares = Column(BigInteger)
    sharesChanged = Column(BigInteger)


class FmpMutualFundHolderSchema(Base):
    __tablename__ = 'fmp_mutual_fund_holder'
    ticker = Column(String(100), primary_key=True, nullable=False)
    holder = Column(String(200), primary_key=True, nullable=False)
    dateReported = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    shares = Column(BigInteger)
    sharesChanged = Column(BigInteger)
    weightPercent = Column(Float)


class FmpEtfHolderSchema(Base):
    """Fmp ETF Holder schema
    """
    __tablename__ = 'fmp_etf_holder'
    asset = Column(String(100), primary_key=True, nullable=True, default='')
    holder = Column(String(100), primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    sharesNumber = Column(BigInteger, nullable=True)
    weightPercentage = Column(Float)


class FmpEnterpriseValueSchema(Base):
    """Fmp Enterprise Value schema
    """
    __tablename__ = 'fmp_enterprise_value'
    symbol = Column(String(100), primary_key=True, nullable=True, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    numberOfShares = Column(BigInteger, nullable=True)
    stockPrice = Column(Float)
    marketCapitalization = Column(Float)
    minusCashAndCashEquivalents = Column(Float)
    addTotalDebt = Column(Float)
    enterpriseValue = Column(Float)


class FmpStockSplitSchema(Base):
    """Fmp Stock Split schema
    """
    __tablename__ = 'fmp_stock_split'
    symbol = Column(String(100), primary_key=True, nullable=True, default='')
    label = Column(String(100), primary_key=True, nullable=True, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    report_date = Column(Date, primary_key=True, nullable=False)
    numerator = Column(Float)
    denominator = Column(Float)


class FmpInsiderTradingSchema(Base):
    """Fmp Insider Trading schema
    """
    __tablename__ = 'fmp_insider_trading'
    symbol = Column(String(100), primary_key=True, nullable=False)
    holder = Column(String(100), primary_key=True, nullable=False)
    transactionDate = Column(Date, primary_key=True, nullable=False)
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    reportingCik = Column(String(100))
    transactionType = Column(String(100))
    securitiesOwned = Column(Float)
    companyCik = Column(String(100))
    reportingName = Column(String(100))
    typeOfOwner = Column(String(100))
    acquistionOrDisposition = Column(String(100))
    formType = Column(String(100))
    securitiesTransacted = Column(Float)
    price = Column(Float)
    securityName = Column(String(100))
    link = Column(String(100))


class FmpCompanyProfileSchema(Base):
    """Fmp Company Profile schema
    """
    __tablename__ = 'fmp_company_profile'
    symbol = Column(String(100), primary_key=True, nullable=False)
    cusip = Column(String(100), primary_key=True, nullable=True, default='')
    row_num = Column(BigInteger, primary_key=True, nullable=False)

    address = Column(String(200))
    beta = Column(Float)
    ceo = Column(String(100))
    changes = Column(Float)
    cik = Column(String(100), nullable=True, default='')
    city = Column(String(100))
    companyName = Column(String(200))
    country = Column(String(100))
    currency = Column(String(100))
    dcf = Column(Float)
    dcfDiff = Column(Float)
    defaultImage = Column(Integer)
    exchange = Column(String(100))
    exchangeShortName = Column(String(100))
    fullTimeEmployees = Column(BigInteger)
    holder = Column(String(100))
    image = Column(String(100))
    industry = Column(String(100))
    ipoDate = Column(Date)
    isActivelyTrading = Column(Integer)
    isEtf = Column(Integer)
    isin = Column(String(100), nullable=True, default='')
    lastDiv = Column(Float)
    mktCap = Column(BigInteger)
    phone = Column(String(100))
    price = Column(Float)
    priceRange = Column(String(100))
    sector = Column(String(100))
    state = Column(String(100))
    volAvg = Column(BigInteger)
    website = Column(String(100))
    zip = Column(String(100))


class FmpSectorPerformanceSchema(Base):
    """Fmp Sector Performance schema
    """
    __tablename__ = 'fmp_sector_performance'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    currentDate = Column(Date, primary_key=True, nullable=False)
    sector = Column(String(100), primary_key=True, nullable=False)
    changes = Column(Float)


class FmpYearlyRatiosSchema(Base):
    __tablename__ = 'fmp_yearly_ratios'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    endDate = Column(Date, primary_key=True, nullable=False)
    period = Column(String(2))
    currentRatio = Column(Float)
    quickRatio = Column(Float)
    cashRatio = Column(Float)
    daysOfSalesOutstanding = Column(Float)
    daysOfInventoryOutstanding = Column(Float)
    operatingCycle = Column(Float)
    daysOfPayablesOutstanding = Column(Float)
    cashConversionCycle = Column(Float)
    grossProfitMargin = Column(Float)
    operatingProfitMargin = Column(Float)
    pretaxProfitMargin = Column(Float)
    netProfitMargin = Column(Float)
    effectiveTaxRate = Column(Float)
    returnOnAssets = Column(Float)
    returnOnEquity = Column(Float)
    returnOnCapitalEmployed = Column(Float)
    netIncomePerEBT = Column(Float)
    ebtPerEbit = Column(Float)
    ebitPerRevenue = Column(Float)
    debtRatio = Column(Float)
    debtEquityRatio = Column(Float)
    longTermDebtToCapitalization = Column(Float)
    totalDebtToCapitalization = Column(Float)
    interestCoverage = Column(Float)
    cashFlowToDebtRatio = Column(Float)
    companyEquityMultiplier = Column(Float)
    receivablesTurnover = Column(Float)
    payablesTurnover = Column(Float)
    inventoryTurnover = Column(Float)
    fixedAssetTurnover = Column(Float)
    assetTurnover = Column(Float)
    operatingCashFlowPerShare = Column(Float)
    freeCashFlowPerShare = Column(Float)
    cashPerShare = Column(Float)
    payoutRatio = Column(Float)
    operatingCashFlowSalesRatio = Column(Float)
    freeCashFlowOperatingCashFlowRatio = Column(Float)
    cashFlowCoverageRatios = Column(Float)
    shortTermCoverageRatios = Column(Float)
    capitalExpenditureCoverageRatio = Column(Float)
    dividendPaidAndCapexCoverageRatio = Column(Float)
    dividendPayoutRatio = Column(Float)
    priceBookValueRatio = Column(Float)
    priceToBookRatio = Column(Float)
    priceToSalesRatio = Column(Float)
    priceEarningsRatio = Column(Float)
    priceToFreeCashFlowsRatio = Column(Float)
    priceToOperatingCashFlowsRatio = Column(Float)
    priceCashFlowRatio = Column(Float)
    priceEarningsToGrowthRatio = Column(Float)
    priceSalesRatio = Column(Float)
    dividendYield = Column(Float)
    enterpriseValueMultiple = Column(Float)
    priceFairValue = Column(Float)


class FmpQuarterlyRatiosSchema(Base):
    __tablename__ = 'fmp_quarterly_ratios'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    endDate = Column(Date, primary_key=True, nullable=False)
    period = Column(String(2))
    currentRatio = Column(Float)
    quickRatio = Column(Float)
    cashRatio = Column(Float)
    daysOfSalesOutstanding = Column(Float)
    daysOfInventoryOutstanding = Column(Float)
    operatingCycle = Column(Float)
    daysOfPayablesOutstanding = Column(Float)
    cashConversionCycle = Column(Float)
    grossProfitMargin = Column(Float)
    operatingProfitMargin = Column(Float)
    pretaxProfitMargin = Column(Float)
    netProfitMargin = Column(Float)
    effectiveTaxRate = Column(Float)
    returnOnAssets = Column(Float)
    returnOnEquity = Column(Float)
    returnOnCapitalEmployed = Column(Float)
    netIncomePerEBT = Column(Float)
    ebtPerEbit = Column(Float)
    ebitPerRevenue = Column(Float)
    debtRatio = Column(Float)
    debtEquityRatio = Column(Float)
    longTermDebtToCapitalization = Column(Float)
    totalDebtToCapitalization = Column(Float)
    interestCoverage = Column(Float)
    cashFlowToDebtRatio = Column(Float)
    companyEquityMultiplier = Column(Float)
    receivablesTurnover = Column(Float)
    payablesTurnover = Column(Float)
    inventoryTurnover = Column(Float)
    fixedAssetTurnover = Column(Float)
    assetTurnover = Column(Float)
    operatingCashFlowPerShare = Column(Float)
    freeCashFlowPerShare = Column(Float)
    cashPerShare = Column(Float)
    payoutRatio = Column(Float)
    operatingCashFlowSalesRatio = Column(Float)
    freeCashFlowOperatingCashFlowRatio = Column(Float)
    cashFlowCoverageRatios = Column(Float)
    shortTermCoverageRatios = Column(Float)
    capitalExpenditureCoverageRatio = Column(Float)
    dividendPaidAndCapexCoverageRatio = Column(Float)
    dividendPayoutRatio = Column(Float)
    priceBookValueRatio = Column(Float)
    priceToBookRatio = Column(Float)
    priceToSalesRatio = Column(Float)
    priceEarningsRatio = Column(Float)
    priceToFreeCashFlowsRatio = Column(Float)
    priceToOperatingCashFlowsRatio = Column(Float)
    priceCashFlowRatio = Column(Float)
    priceEarningsToGrowthRatio = Column(Float)
    priceSalesRatio = Column(Float)
    dividendYield = Column(Float)
    enterpriseValueMultiple = Column(Float)
    priceFairValue = Column(Float)


class FmpRatiosTtmSchema(Base):
    __tablename__ = 'fmp_ratios_ttm'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)  # add during parsing
    endDate = Column(Date, primary_key=True, nullable=False)  # add during parsing
    currentRatioTTM = Column(Float)
    quickRatioTTM = Column(Float)
    cashRatioTTM = Column(Float)
    daysOfSalesOutstandingTTM = Column(Float)
    daysOfInventoryOutstandingTTM = Column(Float)
    operatingCycleTTM = Column(Float)
    daysOfPayablesOutstandingTTM = Column(Float)
    cashConversionCycleTTM = Column(Float)
    grossProfitMarginTTM = Column(Float)
    operatingProfitMarginTTM = Column(Float)
    pretaxProfitMarginTTM = Column(Float)
    netProfitMarginTTM = Column(Float)
    effectiveTaxRateTTM = Column(Float)
    returnOnAssetsTTM = Column(Float)
    returnOnEquityTTM = Column(Float)
    returnOnCapitalEmployedTTM = Column(Float)
    netIncomePerEBTTTM = Column(Float)
    ebtPerEbitTTM = Column(Float)
    ebitPerRevenueTTM = Column(Float)
    debtRatioTTM = Column(Float)
    debtEquityRatioTTM = Column(Float)
    longTermDebtToCapitalizationTTM = Column(Float)
    totalDebtToCapitalizationTTM = Column(Float)
    interestCoverageTTM = Column(Float)
    cashFlowToDebtRatioTTM = Column(Float)
    companyEquityMultiplierTTM = Column(Float)
    receivablesTurnoverTTM = Column(Float)
    payablesTurnoverTTM = Column(Float)
    inventoryTurnoverTTM = Column(Float)
    fixedAssetTurnoverTTM = Column(Float)
    assetTurnoverTTM = Column(Float)
    operatingCashFlowPerShareTTM = Column(Float)
    freeCashFlowPerShareTTM = Column(Float)
    cashPerShareTTM = Column(Float)
    payoutRatioTTM = Column(Float)
    operatingCashFlowSalesRatioTTM = Column(Float)
    freeCashFlowOperatingCashFlowRatioTTM = Column(Float)
    cashFlowCoverageRatiosTTM = Column(Float)
    shortTermCoverageRatiosTTM = Column(Float)
    capitalExpenditureCoverageRatioTTM = Column(Float)
    dividendPaidAndCapexCoverageRatioTTM = Column(Float)
    priceBookValueRatioTTM = Column(Float)
    priceToBookRatioTTM = Column(Float)
    priceToSalesRatioTTM = Column(Float)
    priceEarningsRatioTTM = Column(Float)
    priceToFreeCashFlowsRatioTTM = Column(Float)
    priceToOperatingCashFlowsRatioTTM = Column(Float)
    priceCashFlowRatioTTM = Column(Float)
    priceEarningsToGrowthRatioTTM = Column(Float)
    priceSalesRatioTTM = Column(Float)
    dividendYieldTTM = Column(Float)
    dividendYielTTM = Column(Float)
    dividendYielPercentageTTM = Column(Float)
    dividendPerShareTTM = Column(Float)
    enterpriseValueMultipleTTM = Column(Float)
    priceFairValueTTM = Column(Float)
    dividendPayoutRatio = Column(Float)
    peRatioTTM = Column(Float)
    pegRatioTTM = Column(Float)


class FmpYearlyIncomeStatementSchema(Base):
    __tablename__ = 'fmp_yearly_income_statement'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    endDate = Column(Date, primary_key=True, nullable=False)
    period = Column(String(2))
    reportedCurrency = Column(String(3))
    fillingDate = Column(Date)
    acceptedDate = Column(Date)
    revenue = Column(Float)
    costOfRevenue = Column(Float)
    grossProfit = Column(Float)
    grossProfitRatio = Column(Float)
    researchAndDevelopmentExpenses = Column(Float)
    generalAndAdministrativeExpenses = Column(Float)
    sellingAndMarketingExpenses = Column(Float)
    sellingGeneralAndAdministrativeExpenses = Column(Float)
    otherExpenses = Column(Float)
    operatingExpenses = Column(Float)
    costAndExpenses = Column(Float)
    interestExpense = Column(Float)
    depreciationAndAmortization = Column(Float)
    ebitda = Column(Float)
    ebitdaratio = Column(Float)
    operatingIncome = Column(Float)
    operatingIncomeRatio = Column(Float)
    totalOtherIncomeExpensesNet = Column(Float)
    incomeBeforeTax = Column(Float)
    incomeBeforeTaxRatio = Column(Float)
    incomeTaxExpense = Column(Float)
    netIncome = Column(Float)
    netIncomeRatio = Column(Float)
    eps = Column(Float)
    epsdiluted = Column(Float)
    weightedAverageShsOut = Column(Float)
    weightedAverageShsOutDil = Column(Float)
    link = Column(String(150))
    finalLink = Column(String(150))


class FmpQuarterlyIncomeStatementSchema(Base):
    __tablename__ = 'fmp_quarterly_income_statement'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    endDate = Column(Date, primary_key=True, nullable=False)
    period = Column(String(2))
    reportedCurrency = Column(String(3))
    fillingDate = Column(Date)
    acceptedDate = Column(Date)
    revenue = Column(Float)
    costOfRevenue = Column(Float)
    grossProfit = Column(Float)
    grossProfitRatio = Column(Float)
    researchAndDevelopmentExpenses = Column(Float)
    generalAndAdministrativeExpenses = Column(Float)
    sellingAndMarketingExpenses = Column(Float)
    sellingGeneralAndAdministrativeExpenses = Column(Float)
    otherExpenses = Column(Float)
    operatingExpenses = Column(Float)
    costAndExpenses = Column(Float)
    interestExpense = Column(Float)
    depreciationAndAmortization = Column(Float)
    ebitda = Column(Float)
    ebitdaratio = Column(Float)
    operatingIncome = Column(Float)
    operatingIncomeRatio = Column(Float)
    totalOtherIncomeExpensesNet = Column(Float)
    incomeBeforeTax = Column(Float)
    incomeBeforeTaxRatio = Column(Float)
    incomeTaxExpense = Column(Float)
    netIncome = Column(Float)
    netIncomeRatio = Column(Float)
    eps = Column(Float)
    epsdiluted = Column(Float)
    weightedAverageShsOut = Column(Float)
    weightedAverageShsOutDil = Column(Float)
    link = Column(String(150))
    finalLink = Column(String(150))


class Fmp10QSchema(Base):
    __tablename__ = 'fmp_10_q'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    year = Column(String(4), primary_key=True, nullable=False)
    period = Column(String(2), primary_key=True, nullable=False)
    nMonthsEnded = Column(String(20))
    endingDate = Column(String(20))
    numberOfSharesRepurchased = Column(BigInteger)


class FinnhubSentimentSchema(Base):
    # For sentiment data from reddit
    __tablename__ = 'finnhub_sentiment'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    atTime = Column(String(19), primary_key=True, nullable=False)
    mention = Column(BigInteger)
    positiveScore = Column(Float)
    negativeScore = Column(Float)
    positiveMention = Column(BigInteger)
    negativeMention = Column(BigInteger)
    score = Column(Float)


class FinnhubETFHoldings(Base):
    __tablename__ = 'finnhub_etf_holdings'
    row_num = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(100), primary_key=True, nullable=False)
    atDate = Column(Date, primary_key=True, nullable=False)
    cusip = Column(String(100))
    isin = Column(String(100))
    name = Column(String(200))
    percent = Column(Float)
    share = Column(Float)
    marketValue = Column(Float)
