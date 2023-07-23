import json
symbols = []
for l in open('sym.json'):
    symbols.append(l[:-1])
top100 = [
"ABB",
"ACC",
"ADANIENT",
"ADANIGREEN",
"ADANIPORTS",
"ATGL",
"ADANITRANS",
"AWL",
"AMBUJACEM",
"APOLLOHOSP",
"ASIANPAINT",
"DMART",
"AXISBANK",
"BAJAJ-AUTO",
"BAJFINANCE",
"BAJAJFINSV",
"BAJAJHLDNG",
"BANKBARODA",
"BERGEPAINT",
"BEL",
"BPCL",
"BHARTIARTL",
"BOSCHLTD",
"BRITANNIA",
"CANBK",
"CHOLAFIN",
"CIPLA",
"COALINDIA",
"COLPAL",
"DLF",
"DABUR",
"DIVISLAB",
"DRREDDY",
"EICHERMOT",
"NYKAA",
"GAIL",
"GODREJCP",
"GRASIM",
"HCLTECH",
"HDFCAMC",
"HDFCBANK",
"HDFCLIFE",
"HAVELLS",
"HEROMOTOCO",
"HINDALCO",
"HAL",
"HINDUNILVR",
"HDFC",
"ICICIBANK",
"ICICIGI",
"ICICIPRULI",
"ITC",
"IOC",
"IRCTC",
"INDUSTOWER",
"INDUSINDBK",
"NAUKRI",
"INFY",
"INDIGO",
"JSWSTEEL",
"KOTAKBANK",
"LTIM",
"LT",
"LICI",
"M&M",
"MARICO",
"MARUTI",
"MUTHOOTFIN",
"NTPC",
"NESTLEIND",
"ONGC",
"PIIND",
"PAGEIND",
"PIDILITIND",
"POWERGRID",
"PGHH",
"RELIANCE",
"SBICARD",
"SBILIFE",
"SRF",
"MOTHERSON",
"SHREECEM",
"SIEMENS",
"SBIN",
"SUNPHARMA",
"TCS",
"TATACONSUM",
"TATAMOTORS",
"TATAPOWER",
"TATASTEEL",
"TECHM",
"TITAN",
"TORNTPHARM",
"UPL",
"ULTRACEMCO",
"MCDOWELL-N",
"VBL",
"VEDL",
"WIPRO",
"ZOMATO"]

res = {}

for s in top100:
    print(f"ssssssssssss: {s}")
    found = 0
    for s_ft in symbols:
        if s_ft.find('"exch_seg":"NSE"') == -1: continue
        if s_ft.find("-EQ") == -1: continue
        if s_ft.find('"symbol":"' + s + '-EQ"') != -1:
            print(f"{s}:{s_ft}")
            found += 1
            res[s] = s_ft

    if found == 0:
        print(f"ERROR: no FT symbol found for {s}")
    elif found > 1:
        print(f"ERROR: More than one({found}) FT symbol found for {s}")

b=""
for s,r in res.items():
    r = json.loads(r)
    b += f"NSE|{r['token']}#" 
print("==============================")
print(b)
print("==============================")
