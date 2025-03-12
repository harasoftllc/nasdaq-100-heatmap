import yfinance as yf
import pandas as pd

# NASDAQ-100 tickers (as of March 2025, verify periodically)
nasdaq_100_tickers = [
    'AAPL', 'ABNB', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AMAT', 'AMD', 'AMGN',
    'AMZN', 'ANSS', 'APP', 'ARM', 'ASML', 'AVGO', 'AXON', 'AZN', 'BIIB', 'BKNG',
    'BKR', 'CCEP', 'CDNS', 'CDW', 'CEG', 'CHTR', 'CMCSA', 'COST', 'CPRT', 'CRWD',
    'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'DASH', 'DDOG', 'DXCM', 'EA', 'EXC',
    'FANG', 'FAST', 'FTNT', 'GEHC', 'GFS', 'GILD', 'GOOG', 'GOOGL', 'HON', 'IDXX',
    'INTC', 'INTU', 'ISRG', 'KDP', 'KHC', 'KLAC', 'LIN', 'LRCX', 'LULU', 'MAR',
    'MCHP', 'MDB', 'MDLZ', 'MELI', 'META', 'MNST', 'MRVL', 'MSFT', 'MSTR', 'MU',
    'NFLX', 'NVDA', 'NXPI', 'ODFL', 'ON', 'ORLY', 'PANW', 'PAYX', 'PCAR', 'PDD',
    'PEP', 'PLTR', 'PYPL', 'QCOM', 'REGN', 'ROP', 'ROST', 'SBUX', 'SNPS', 'TEAM',
    'TMUS', 'TSLA', 'TTD', 'TTWO', 'TXN', 'VRSK', 'VRTX', 'WBD', 'WDAY', 'XEL', 'ZS'
]


# Fetch NASDAQ-100 data
def fetch_nasdaq_data(tickers):
    data = []
    tickers_str = ' '.join(tickers)
    stocks = yf.download(tickers_str, period="2d", group_by='ticker', threads=True)

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            market_cap = info.get('marketCap', None)

            # Get closing prices to calculate daily % change
            close_yesterday = stocks[ticker]['Close'].iloc[-2]
            close_today = stocks[ticker]['Close'].iloc[-1]
            percent_change = round(((close_today - close_yesterday) / close_yesterday) * 100, 2)

            data.append({
                'ticker': ticker,
                'market_cap': market_cap,
                'percent_change': percent_change
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    df = pd.DataFrame(data).dropna()
    return df

# Run and save the data
nasdaq_df = fetch_nasdaq_data(nasdaq_100_tickers)
nasdaq_df.to_csv('nasdaq100_data.csv', index=False)

# print(nasdaq_df.head())
