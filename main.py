from functions import black_scholes, mispricing, confirmed_mispricing, heston_price
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf

def get_yfinance_options(ticker, action, option_types):
    stock = yf.Ticker(ticker)
    expirations = stock.options
    today = datetime.utcnow()

    heston_params = {
        'kappa': 2.0,
        'theta': 0.04,
        'sigma': 0.3,
        'rho': -0.7,
        'v0': 0.04
    }

    valid_options = []

    for exp in expirations:
        try:
            exp_date = datetime.strptime(exp, "%Y-%m-%d")
            dte = (exp_date - today).days
            if not (30 <= dte <= 45):
                continue

            chain = stock.option_chain(exp)
            underlying_price = stock.history(period="1d")['Close'].iloc[-1]

            for option_type in option_types:
                options_df = chain.calls if option_type == 'call' else chain.puts

                for _, row in options_df.iterrows():
                    strike = row['strike']
                    iv = row['impliedVolatility']
                    T = dte / 365
                    r = 0.045
                    S = underlying_price
                    market_price = row['ask'] if action == 'buy' else row['bid']

                    if np.isnan(market_price) or market_price == 0 or np.isnan(iv):
                        continue

                    bs_result = mispricing(S, strike, T, r, iv, market_price, option_type, action=action)
                    if not bs_result['signal']:
                        continue

                    heston_result = confirmed_mispricing(S, strike, T, r, iv, market_price, option_type, action, heston_params)
                    if heston_result['signal']:
                        valid_options.append({
                            'ticker': ticker.upper(),
                            'option_type': option_type,
                            'action': action,
                            'strike': strike,
                            'expiration': exp_date.strftime("%Y-%m-%d"),
                            'dte': dte,
                            'bs_price': round(bs_result['bs_price'], 4),
                            'heston_price': round(heston_result['heston_price'], 4),
                            'market_price': round(market_price, 4),
                            'bs_mispricing_pct': round(bs_result['misprice_pct'], 4),
                            'heston_mispricing_pct': round(heston_result['misprice_pct'], 4),
                            'implied_vol': round(iv, 4)
                        })

        except Exception as e:
            print(f"Error processing expiration {exp}: {e}")

    return pd.DataFrame(valid_options)