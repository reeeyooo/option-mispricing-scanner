import streamlit as st
from functions import black_scholes, mispricing, confirmed_mispricing, heston_price
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
from main import get_yfinance_options  # keep this import if needed elsewhere

st.title("Option Mispricing Scanner")

ticker = st.text_input("Enter ticker (e.g. SPY)")
action = st.radio("Action", ["buy", "sell"])
option_types = st.multiselect("Option Type(s)", ["call", "put"], default=["call"])

if st.button("Scan Options"):
    if not ticker:
        st.error("Please enter a valid ticker.")
    elif not option_types:
        st.error("Please select at least one option type.")
    else:
        st.info("Scanning... This may take a few seconds.")
        results_df = get_yfinance_options(ticker.upper(), action, option_types)

        if results_df.empty:
            st.warning("No valid mispricings found.")
        else:
            st.success(f"Found {len(results_df)} valid opportunities!")
            st.dataframe(results_df)

            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name=f"{ticker}_{action}_mispricings.csv",
                mime='text/csv'
            )