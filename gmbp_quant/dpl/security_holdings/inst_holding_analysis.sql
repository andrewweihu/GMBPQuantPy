WITH JOIN_PRICE AS
(
    SELECT
      a.price,
      a.mktCap,
      a.cusip,
      a.symbol,
      b.reportDate,
      b.adjustedNumShares,
      b.CIK,
      b.institutionName,
      a.price * b.adjustedNumShares AS shareValue
    FROM mktdata.fmp_company_profile AS a
    JOIN mktdata.matview_sec13f_holding_trend AS b
    ON a.cusip = b.CUSIP
),
TOP_INST AS
(
    SELECT
      CIK,
      institutionName,
      SUM(shareValue) AS shareValue
    FROM JOIN_PRICE
    WHERE reportDate = '2021-03-31'
    GROUP BY CIK, institutionName
    ORDER BY shareValue DESC
    LIMIT 50
),
TOP_ALL AS (
    SELECT JOIN_PRICE.*
    FROM JOIN_PRICE
    JOIN TOP_INST
    ON JOIN_PRICE.CIK = TOP_INST.CIK
),
TOP_ALL_NUM AS(
    SELECT
        ROW_NUMBER() OVER (PARTITION BY reportDate, CIK ORDER BY shareValue DESC) AS row_num,
        reportDate,
        CIK,
        symbol,
        mktCap,
        institutionName,
        adjustedNumShares,
        shareValue
    FROM TOP_ALL
),
FINAL AS (
  SELECT * FROM TOP_ALL_NUM WHERE row_num <= 50
)
SELECT
  symbol,
  reportDate,
  mktCap,
  count(*) as numHolders,
  sum(adjustedNumShares) AS totalAdjustedNumShares,
  sum(shareValue) AS totalHoldingValue
FROM FINAL
GROUP BY symbol, reportDate, mktCap
;
