# Option Mispricing Scanner

A Streamlit app that identifies potentially mispriced options using Black-Scholes and Heston models.

# Features

- Scan for mispriced options by ticker
- Filter by buy/sell opportunities
- Export results to CSV

# Installation

1. Clone the repo:
git clone https://github.com/reeeyooo/option-mispricing-scanner

2. Navigate into the directory:
cd option-mispricing-scanner

3. Set up a virtual environment (recommended):
python -m venv venv
source venv/bin/activate (or venv\Scripts\activate on Windows)

4. Install dependencies:
pip install -r requirements.txt

5. Run code and enter, streamlit run app.py, in the terminal

# Usage
- Enter a ticker symbol (e.g., SPY)
- Results will show mispriced options meeting the threshold criteria
- You can download results as CSV

# Output columns
- bs_price:	               Black-Scholes calculated price
- heston_price:	         Heston model calculated price
- market_price:	         Actual market price
- bs_mispricing_pct:	      BS model mispricing percentage
- heston_mispricing_pct:	Heston model mispricing percentage