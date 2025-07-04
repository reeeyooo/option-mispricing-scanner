import streamlit as st
from main import get_yfinance_options  
import pandas as pd

st.title("Option Mispricing Scanner")

ticker = st.text_input("Enter ticker (e.g. SPY)")
action = st.radio("Action", ["buy", "sell"])

if st.button("Scan Options"):
    if not ticker:
        st.error("Please enter a valid ticker.")
    else:
        st.info("Scanning... This may take a few seconds.")
        results_df = get_yfinance_options(ticker.upper(), action)

        if results_df.empty:
            st.warning("No valid mispricings found.")
        else:
            st.success(f"Found {len(results_df)} valid opportunities!")
            st.dataframe(results_df)

            # Download as CSV
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name=f"{ticker}_{action}_mispricings.csv",
                mime='text/csv'
            )
