import json
import pandas as pd

with open("/Users/ariel/Documents/GitHub/GMBPQuantPy/gmbp_quant/fmp_data/10-Q/2020-Q4-AAPL-json.txt", 'r') as json_file:
    data = json.load(json_file)
    ticker = "AAPL"
    year = 2020
    quarter = "Q4"

    results = {"symbol": [ticker, ticker], "year": [year, year], "period": [quarter, quarter]}
    for outer_key in data:
        if "CONDENSED CONSOLIDATED STATEM" not in outer_key:
            continue
        elements = data[outer_key]
        if "CASH FLOWS" not in list(elements[0].keys())[0]:
            continue
        nMonthsEnded = list(elements[0].values())[0][0]
        ending_dates = []
        numberOfSharesRepurchased = []
        for element in elements:
            if "items" in list(element.keys())[0]:
                endingDate = list(element.values())[0]
            if "Repurchases of common stock".upper() in list(element.keys())[0].upper():
                numberOfSharesRepurchased = list(element.values())[0]
        if len(endingDate) == 2 and len(numberOfSharesRepurchased) == 2:
            results["nMonthsEnded"] = [nMonthsEnded, nMonthsEnded]
            results["endingDate"] = endingDate
            results["numberOfSharesRepurchased"] = numberOfSharesRepurchased
            break
    print(results)
        # table = pd.DataFrame(elements)
        # for element in data[outer_key]:
        #     for inner_key in element:
        #         print(f"----{inner_key}")
    # print(data["symbol"])
    # print("CONDENSED CONSOLIDATED STATEM_4" in data)
    # print(data["CONDENSED CONSOLIDATED STATEM_4"][0])
    # print(data["CONDENSED CONSOLIDATED STATEM_4"][26])
    # # table = pd.DataFrame(data)
    # # table.head()
