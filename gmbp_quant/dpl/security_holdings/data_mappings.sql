DROP VIEW mktdata.view_etf_holding_detail;
CREATE VIEW mktdata.view_etf_holding_detail AS
WITH A AS 
(
	 SELECT 
	 x.asset, x.holder, MAX(x.sharesNumber) AS holding_shares, MAX(y.mktCap) AS holder_mktCap 
	 FROM mktdata.fmp_etf_holder AS X
		 JOIN mktdata.fmp_company_profile AS Y
		 ON X.holder = Y.symbol
	 WHERE mktCap > 1000000 AND Y.IsEtf = 1 AND (Y.exchangeShortName = 'NASDAQ' OR Y.exchangeShortName = 'NYSE')
	 GROUP BY asset, holder
),
B AS
(
    SELECT 
        symbol, mktCap / price AS total_shares, mktCap 
    FROM mktdata.fmp_company_profile 
    WHERE price > 0 AND mktCap > 1000000 AND IsEtf = 0 AND (exchangeShortName = 'NASDAQ' OR exchangeShortName = 'NYSE')
)
SELECT 
    A.*, B.*,
    B.mktCap/B.total_shares * A.holding_shares > A.holder_mktCap AS suspicious
FROM A
JOIN B
ON A.asset = B.symbol
;

DROP VIEW mktdata.view_etf_percentage;
CREATE VIEW mktdata.view_etf_percentage AS
SELECT 
    asset, 
    SUM(holding_shares) AS etf_shares,
    MAX(mktCap)  AS mktCap,
    MAX(total_shares) AS total_shares,
    SUM(holding_shares) / MAX(total_shares) AS percentage
FROM mktdata.view_etf_holding_detail
WHERE mktCap > 1000000000 AND holder_mktCap > 1000000000 AND holding_shares > 0 AND suspicious = 0
GROUP BY asset
;

