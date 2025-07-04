# Option Mispricing Scanner

A Streamlit app that scans for potentially mispriced options using Black-Scholes and Heston models.

## How to Run

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Usage
- Enter a ticker symbol (e.g., SPY)
- Select whether you want to scan for buying or selling opportunities
- Click "Scan Options"
- Results will show mispriced options meeting the threshold criteria
- You can download results as CSV

## Models Used
- Black-Scholes for initial screening
- Heston model for confirmation