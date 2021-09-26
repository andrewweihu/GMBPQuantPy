--------------------------------------------------------
-- MySQL logic to build foundation views/temp tables
-- for institution security holdings. Given a ticker,
-- we expect a list of institutes having this ticker in
-- their holdings with quarter over quarter change.
--------------------------------------------------------

-- Create CUSIP <-> Ticker mapping
DROP VIEW IF EXISTS mktdata.view_cusip_ticker_mapping;
CREATE VIEW mktdata.view_cusip_ticker_mapping AS
    SELECT
        cusip AS cusip,
        max(symbol) AS symbol
    FROM mktdata.fmp_company_profile
    WHERE exchangeShortName IN ('NYSE', 'NASDAQ')
        AND cusip <> ''
        AND symbol <> ''
    GROUP BY 1
;


-- Create CIK <-> Institute mapping from FMP company profile
-- Note: This may not have all CIK that show up in 13F
DROP VIEW IF EXISTS mktdata.view_cik_company_mapping;
CREATE VIEW mktdata.view_cik_company_mapping AS
    SELECT
        cik,
        max(companyName) AS companyName,
        max(country) AS country,
        max(industry) AS industry,
        max(sector) AS sector
    FROM mktdata.fmp_company_profile
    WHERE exchangeShortName IN ('NYSE', 'NASDAQ')
        AND cik <> ''
        AND companyName <> ''
    GROUP BY 1
;


-- Create unique CIK <-> Institute name mapping from mapped 13F
DROP VIEW IF EXISTS mktdata.view_cik_name_mapping;
CREATE VIEW mktdata.view_cik_name_mapping AS
    SELECT
        cik,
        max(company_name) AS holding_company_name
    FROM mktdata.fmp_sec_cik_name
    GROUP BY 1
;


-- Get cumulative split factor to get the multiplier for security shares
DROP VIEW IF EXISTS mktdata.view_cumulative_splits;
CREATE VIEW mktdata.view_cumulative_splits AS
    WITH log_split_factor AS (
        SELECT
            symbol,
            report_date,
            numerator,
            -- Add ROW_NUMBER window function to avoid incorrect MySQL window function operations
            -- Test case: symbol = 'TSLA'
            ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY report_date DESC) AS row_n1,
            sum(log(numerator)) OVER (PARTITION BY symbol ORDER BY report_date DESC) AS cum_numerator,
            denominator,
            -- Add ROW_NUMBER window function to avoid incorrect MySQL window function operations
            -- Test case: symbol = 'TSLA'
            ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY report_date DESC) AS row_n2,
            sum(log(denominator)) OVER (PARTITION BY symbol ORDER BY report_date DESC) AS cum_denominator
        FROM mktdata.fmp_stock_split
        WHERE numerator > 0
    )
    SELECT
        mapp.cusip,
        lsf.symbol,
        lsf.report_date,
        lsf.numerator,
        round(exp(lsf.cum_numerator), 0) AS cum_numerator,
        lsf.denominator,
        round(exp(lsf.cum_denominator), 0) AS cum_denominator
    FROM log_split_factor lsf
    LEFT JOIN mktdata.view_cusip_ticker_mapping mapp
    ON lsf.symbol = mapp.symbol
;


-- Get adjusted total number of shares for securities
DROP VIEW IF EXISTS mktdata.view_split_adjusted_security_shares;
CREATE VIEW mktdata.view_split_adjusted_security_shares AS
    WITH shares_splits_temp AS (
        SELECT
            mapp.cusip,
            val.symbol,
            val.report_date,
            spl.report_date AS split_date,
            val.numberOfShares AS total_shares,
            spl.cum_numerator,
            spl.cum_denominator,
            val.numberOfShares * COALESCE(spl.cum_numerator, 1) / COALESCE(spl.cum_denominator, 1) AS adjusted_total_shares,
            ROW_NUMBER() OVER (PARTITION BY val.symbol, val.report_date ORDER BY spl.report_date) AS row_num
        FROM mktdata.fmp_enterprise_value val
        LEFT JOIN mktdata.view_cumulative_splits spl
        ON val.symbol = spl.symbol
            AND val.report_date < spl.report_date
        JOIN mktdata.view_cusip_ticker_mapping mapp
        ON val.symbol = mapp.symbol
    )
    SELECT
        *
    FROM shares_splits_temp
    WHERE row_num = 1
;


-- Union 13F and 13F amendment filing and reduce to end state of position holdings
DROP VIEW mktdata.view_13f_union;
CREATE VIEW mktdata.view_13f_union AS
WITH sec13f_union AS (
    SELECT
        '13FHR' AS form,
        0 AS amendment_num,
        'NA' AS amendment_type,
        report_date,
        date_as_of_change,
        row_num,
        cik,
        cusip,
        ssh_prn_type,
        ssh_prn_amt,
        put_call
    FROM mktdata.sec_13fhr
    UNION
    SELECT
        '13FHRA' AS form,
        COALESCE(amendment_num, 1) AS amendment_num,
        COALESCE(amendment_type, 'RESTATEMENT') AS amendment_type,
        report_date,
        date_as_of_change,
        row_num,
        cik,
        cusip,
        ssh_prn_type,
        ssh_prn_amt,
        put_call
    FROM mktdata.sec_13fhra
),
ranked_union AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY report_date, row_num, cik, cusip ORDER BY amendment_num DESC, date_as_of_change DESC) AS rn
    FROM sec13f_union
)
SELECT *
FROM ranked_union
WHERE
    -- when the last filing is original filing (NA) or restatement we only need the last holding positions
    (rn = 1 AND amendment_type IN ('NA', 'RESTATEMENT'))
    -- when the last filing is new holdings we need to include the previous holding positions
    OR ((rn = 1 AND amendment_type = 'NEW HOLDINGS') OR (rn = 2 AND amendment_type <> 'NEW HOLDINGS'))
;


-- Roll up holdings to date, CIK, CUSIP as one institute can have the same CUSIP on multiple lines for the same report date
DROP VIEW IF EXISTS mktdata.view_sec13f_institute_holdings;
CREATE VIEW mktdata.view_sec13f_institute_holdings AS
    SELECT
        report_date,
        cik,
        cusip,
        sum(ssh_prn_amt) AS num_shares
    FROM mktdata.view_13f_union
    WHERE ssh_prn_type = 'SH'
        AND put_call IS NULL
    GROUP BY 1, 2, 3
;


-- Get adjusted number of shares as of SEC 13F report date
DROP VIEW IF EXISTS mktdata.view_sec13f_institute_holdings_split_adjusted;
CREATE VIEW mktdata.view_sec13f_institute_holdings_split_adjusted AS
    WITH institute_shares AS (
        SELECT
            hld.report_date,
            hld.cik,
            hld.cusip,
            spl.symbol,
            hld.num_shares,
            spl.report_date AS earliest_split_date,
            spl.cum_numerator,
            spl.cum_denominator,
            hld.num_shares * COALESCE(spl.cum_numerator, 1) / COALESCE(spl.cum_denominator, 1) AS adjusted_num_shares,
            ROW_NUMBER() OVER (PARTITION BY hld.report_date, hld.cik, hld.cusip ORDER BY spl.report_date) AS row_n
        FROM mktdata.view_sec13f_institute_holdings hld
        LEFT JOIN mktdata.view_cumulative_splits spl
        ON hld.cusip = spl.cusip
            AND hld.report_date < spl.report_date
    )
    SELECT *
    FROM institute_shares
    WHERE row_n = 1
;


-- Get adjusted number of shares as of SEC 13F report date and total adjusted number of shares of securities
DROP VIEW IF EXISTS mktdata.view_sec13f_institute_holdings_total_shares_split_adjusted;
CREATE VIEW mktdata.view_sec13f_institute_holdings_total_shares_split_adjusted AS
    WITH institute_shares AS (
        SELECT
            hld.report_date,
            shr.report_date AS latest_total_shares_date,
            hld.earliest_split_date,
            hld.cik,
            hld.cusip,
            hld.num_shares,
            hld.cum_numerator,
            hld.adjusted_num_shares,
            shr.symbol,
            shr.total_shares,
            shr.adjusted_total_shares,
            ROW_NUMBER() OVER (PARTITION BY hld.report_date, hld.cik, hld.cusip ORDER BY shr.report_date DESC) AS row_n
        FROM mktdata.view_sec13f_institute_holdings_split_adjusted hld
        LEFT JOIN mktdata.view_split_adjusted_security_shares shr
        ON hld.cusip = shr.cusip
            AND hld.report_date >= shr.report_date
        -- Specific case to speed up metric dev
        -- WHERE hld.cik = '0001697748'
        -- ORDER BY hld.report_date DESC, shr.symbol, shr.report_date
    )
    SELECT *
    FROM institute_shares
    WHERE row_n = 1
;


-- Create foundation view for trusted.institutional_holding
DROP VIEW IF EXISTS mktdata.view_sec13f_holding_trend;
CREATE VIEW mktdata.view_sec13f_holding_trend AS
    SELECT
        ins.symbol AS ticker,
        ins.cusip AS CUSIP,
        ins.latest_total_shares_date AS latestTotalSharesDate,
        ins.total_shares AS totalShares,
        ins.adjusted_total_shares AS adjustedTotalShares,
        ins.report_date AS reportDate,
        ins.cik AS CIK,
        cikcom.holding_company_name AS institutionName,
        ins.num_shares AS numOfShares,
        ins.adjusted_num_shares AS adjustedNumShares,
        ins.adjusted_num_shares / nullif(ins.adjusted_total_shares, 0) AS percentage,
        ins.adjusted_num_shares - preins.adjusted_num_shares AS sharesChange,
        ins.adjusted_num_shares / nullif(ins.adjusted_total_shares, 0) - preins.adjusted_num_shares / nullif(preins.adjusted_total_shares, 0) AS percentChange
    FROM mktdata.view_sec13f_institute_holdings_total_shares_split_adjusted AS ins
    LEFT JOIN mktdata.view_sec13f_institute_holdings_total_shares_split_adjusted AS preins
    ON ins.cik = preins.cik
        AND ins.cusip = preins.cusip
        AND LAST_DAY(preins.report_date + INTERVAL 1 QUARTER) = ins.report_date
    LEFT JOIN mktdata.view_cik_name_mapping cikcom
    ON ins.cik = cikcom.cik
;


-- Create foundation view for trusted.institution_profile
DROP VIEW IF EXISTS mktdata.view_institution_profile;
CREATE VIEW mktdata.view_institution_profile AS
    SELECT
        cik AS CIK,
        companyName AS institutionName,
        'NA' AS institutionType,
        country AS country
    FROM mktdata.view_cik_company_mapping
;

-------------------------
------- Materialize -----
-------------------------
CREATE TABLE mktdata.matview_sec13f_holding_trend(
    ticker varchar(100) ,
    CUSIP varchar(100) ,
    latestTotalSharesDate date ,
    totalShares bigint(20) ,
    adjustedTotalShares double(17,0) ,
    reportDate date ,
    CIK varchar(100) ,
    institutionName varchar(500) ,
    numOfShares decimal(41,0) ,
    adjustedNumShares double(17,0) ,
    percentage double(22,4) ,
    sharesChange double(22,0) ,
    percentChange double(22,4)
);
INSERT INTO mktdata.matview_sec13f_holding_trend 
SELECT * from mktdata.view_sec13f_holding_trend

-------------------------
------- Testing ---------
-------------------------
-- Test with TSLA
SELECT * 
FROM mktdata.view_sec13f_holding_trend
WHERE ticker = 'TSLA'
ORDER BY reportDate DESC, numOfShares DESC
;


-- Test on CIK holding institution profile
SELECT *
FROM mktdata.view_institution_profile
;
