from sec_api import QueryApi

queryApi = QueryApi(api_key="647eb2101ad1abaebc349de432b498811306bb0a14e730c5782cb8c8b1817ee1")

query = {
  "query": { "query_string": {
      "query": "ticker:TSLA AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-Q\""
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

print(filings)