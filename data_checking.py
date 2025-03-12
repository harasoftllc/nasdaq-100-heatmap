import pandas as pd
from itertools import zip_longest
from ace_tools_open import display_dataframe_to_user

# List provided by user (tickers from NASDAQ-100 as of March 11, 2025)
nasdaq_100_tickers_user_provided = [
    'AAPL', 'ABNB', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AMAT', 'AMD', 'AMGN',
    'AMZN', 'ANSS', 'APP', 'ARM', 'ASML', 'AVGO', 'AXON', 'AZN', 'BIIB', 'BKNG',
    'BKR', 'CCEP', 'CDNS', 'CDW', 'CEG', 'CHTR', 'CMCSA', 'COST', 'CPRT', 'CRWD',
    'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'DASH', 'DDOG', 'DXCM', 'EA', 'EXC',
    'FANG', 'FAST', 'FTNT', 'GEHC', 'GFS', 'GILD', 'GOOG', 'GOOGL', 'HON', 'IDXX',
    'INTC', 'INTU', 'ISRG', 'KDP', 'KHC', 'KLAC', 'LIN', 'LRCX', 'LULU', 'MAR',
    'MCHP', 'MDB', 'MDLZ', 'MELI', 'META', 'MNST', 'MRVL', 'MSFT', 'MSTR', 'MU',
    'NFLX', 'NVDA', 'NXPI', 'ODFL', 'ON', 'ORLY', 'PANW', 'PAYX', 'PCAR', 'PDD',
    'PEP', 'PLTR', 'PYPL', 'QCOM', 'REGN', 'ROP', 'SBUX', 'SNPS', 'TMUS', 'TSLA',
    'TTD', 'TTWO', 'TXN', 'VRSK', 'VRTX', 'WBD', 'WDAY', 'XEL', 'ZS', 'APP', 'ARM', 'GFS', 'GEHC', 'NFLX', 'NVDA', 'NXPI', 'ODFL', 'ON', 'ORLY', 'PANW'
]

# List from CSV (provided previously)
nasdaq_csv_output = pd.read_csv('nasdaq100_data.csv')
csv_tickers = nasdaq_csv_output['ticker'].tolist()

# Identify discrepancies
unexpected_items = set(nasdaq_100_tickers_user_provided) - set(csv_tickers)
missing_items = set(csv_tickers) - set(nasdaq_100_tickers_user_provided)

# Display discrepancies
df_discrepancy = pd.DataFrame(list(zip_longest(
    unexpected_items, missing_items, fillvalue=''
)),

columns=['Unexpected Items (Missing in CSV)', 'Missing Items (Extra in CSV)'])

display_dataframe_to_user(name="NASDAQ-100 Ticker Discrepancies", dataframe=df_discrepancy)
