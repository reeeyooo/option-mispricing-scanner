import scipy.stats as si
import numpy as np
from scipy.integrate import quad

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        return S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)


def mispricing(S, K, T, r, sigma, market_price, option_type='call', action='buy', threshold=0.15):
    bs_price = black_scholes(S, K, T, r, sigma, option_type)
    
    if action == 'buy':
        misprice_pct = (bs_price - market_price) / bs_price
    else:  # sell
        misprice_pct = (market_price - bs_price) / bs_price

    signal = abs(misprice_pct) > threshold
    return {
        'bs_price': bs_price,
        'misprice_pct': abs(misprice_pct * 100),
        'signal': signal
    }

def confirmed_mispricing(S, K, T, r, sigma, market_price, option_type, action, heston_params, threshold=0.10):
    heston_val = heston_price(S, K, T, r, **heston_params, option_type=option_type)

    if abs(heston_val) < 1e-6:  # avoid dividing by zero or near-zero values
        return {
            'heston_price': heston_val,
            'misprice_pct': float('inf'),
            'signal': False
        }

    if action == 'buy':
        misprice_pct = abs((heston_val - market_price) / heston_val)
    else:
        misprice_pct = abs((market_price - heston_val) / heston_val)

    signal = abs(misprice_pct) > threshold
    return {
        'heston_price': heston_val,
        'misprice_pct': abs(misprice_pct * 100),
        'signal': signal
    }



def heston_char_func(phi, S, K, T, r, kappa, theta, sigma, rho, v0, lambda_=0, Pnum=1):
    x = np.log(S)
    a = kappa * theta
    u = 0.5 if Pnum == 1 else -0.5
    b = kappa + lambda_ - rho * sigma if Pnum == 2 else kappa + lambda_
    d = np.sqrt((rho * sigma * phi * 1j - b)**2 - sigma**2 * (2 * u * phi * 1j - phi**2))
    g = (b - rho * sigma * phi * 1j + d) / (b - rho * sigma * phi * 1j - d)

    C = r * phi * 1j * T + (a / sigma**2) * ((b - rho * sigma * phi * 1j + d) * T - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g)))
    D = ((b - rho * sigma * phi * 1j + d) / sigma**2) * ((1 - np.exp(d * T)) / (1 - g * np.exp(d * T)))

    return np.exp(C + D * v0 + 1j * phi * x)

# Integrand for probability P1 and P2
def heston_integrand(phi, S, K, T, r, kappa, theta, sigma, rho, v0, lambda_, Pnum):
    cf = heston_char_func(phi, S, K, T, r, kappa, theta, sigma, rho, v0, lambda_, Pnum)
    return np.real(np.exp(-1j * phi * np.log(K)) * cf / (1j * phi))

# Heston price computation
def heston_price(S, K, T, r, kappa, theta, sigma, rho, v0, option_type='call'):
    P1 = 0.5 + (1 / np.pi) * quad(lambda phi: heston_integrand(phi, S, K, T, r, kappa, theta, sigma, rho, v0, 0, 1), 1e-6, 50)[0]
    P2 = 0.5 + (1 / np.pi) * quad(lambda phi: heston_integrand(phi, S, K, T, r, kappa, theta, sigma, rho, v0, 0, 2), 1e-6, 50)[0]


    call_price = S * P1 - K * np.exp(-r * T) * P2
    if np.isnan(call_price) or call_price < 0:
        call_price = 0

    if option_type == 'call':
        return call_price
    else:
        put_price = call_price + K * np.exp(-r * T) - S
        return put_price