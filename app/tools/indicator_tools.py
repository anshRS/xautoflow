from typing import List, Dict
import pandas as pd
import pandas_ta as ta
from functools import partial

def parse_indicator_config(indicator: str) -> tuple:
    """Parse indicator string into name and parameters."""
    parts = indicator.split('_')
    name = parts[0].lower()
    params = [int(p) for p in parts[1:]]
    return name, params

def calculate_indicators(
    data: List[Dict],
    indicator_config: List[str]
) -> Dict:
    """Calculate technical indicators from market data."""
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        
        results = {}
        for indicator in indicator_config:
            name, params = parse_indicator_config(indicator)
            
            if name == "rsi":
                results[indicator] = ta.rsi(df['close'], length=params[0]).tolist()
            
            elif name == "macd":
                macd = ta.macd(
                    df['close'],
                    fast=params[0],
                    slow=params[1],
                    signal=params[2]
                )
                results[indicator] = {
                    "macd": macd["MACD_" + str(params[0]) + "_" + str(params[1]) + "_" + str(params[2])].tolist(),
                    "signal": macd["MACDs_" + str(params[0]) + "_" + str(params[1]) + "_" + str(params[2])].tolist(),
                    "histogram": macd["MACDh_" + str(params[0]) + "_" + str(params[1]) + "_" + str(params[2])].tolist()
                }
            
            elif name == "sma":
                results[indicator] = ta.sma(df['close'], length=params[0]).tolist()
            
            elif name == "ema":
                results[indicator] = ta.ema(df['close'], length=params[0]).tolist()
            
            elif name == "bbands":
                bbands = ta.bbands(df['close'], length=params[0])
                results[indicator] = {
                    "upper": bbands["BBU_" + str(params[0]) + "_2.0"].tolist(),
                    "middle": bbands["BBM_" + str(params[0]) + "_2.0"].tolist(),
                    "lower": bbands["BBL_" + str(params[0]) + "_2.0"].tolist()
                }
        
        return {
            "success": True,
            "indicators": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }