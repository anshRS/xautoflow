import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.tools.market_data_api_tool import get_market_data

def calculate_technical_indicators(symbol: str, indicators: List[str]) -> Dict[str, Any]:
    """
    Calculate technical indicators for a given symbol.
    
    Args:
        symbol: The stock symbol
        indicators: List of indicators to calculate
        
    Returns:
        Dictionary containing the calculated indicators
    """
    # Get historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    df = get_market_data(symbol, start_date, end_date)
    
    results = {}
    
    for indicator in indicators:
        if indicator.lower() == 'rsi':
            results['rsi'] = df.ta.rsi().iloc[-1]
        elif indicator.lower() == 'macd':
            macd = df.ta.macd()
            results['macd'] = {
                'macd': macd['MACD_12_26_9'].iloc[-1],
                'signal': macd['MACDs_12_26_9'].iloc[-1],
                'histogram': macd['MACDh_12_26_9'].iloc[-1]
            }
        elif indicator.lower() == 'bollinger':
            bollinger = df.ta.bbands()
            results['bollinger'] = {
                'upper': bollinger['BBU_20_2.0'].iloc[-1],
                'middle': bollinger['BBM_20_2.0'].iloc[-1],
                'lower': bollinger['BBL_20_2.0'].iloc[-1]
            }
    
    return results

def fetch_historical_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical price data for a given symbol.
    
    Args:
        symbol: The stock symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        DataFrame containing historical price data
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return get_market_data(symbol, start, end)

def optimize_strategy_parameters(symbol: str, strategy_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimize trading strategy parameters.
    
    Args:
        symbol: The stock symbol
        strategy_type: Type of trading strategy
        parameters: Strategy parameters to optimize
        
    Returns:
        Dictionary containing optimized parameters
    """
    # Get historical data for optimization
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    df = get_market_data(symbol, start_date, end_date)
    
    # Simple optimization example (can be expanded based on strategy type)
    if strategy_type.lower() == 'moving_average':
        best_period = 20  # Default
        best_sharpe = -float('inf')
        
        for period in range(10, 51, 5):
            df['MA'] = df['Close'].rolling(window=period).mean()
            df['Returns'] = df['Close'].pct_change()
            df['Strategy_Returns'] = df['Returns'].shift(-1) * (df['Close'] > df['MA']).astype(int)
            sharpe = df['Strategy_Returns'].mean() / df['Strategy_Returns'].std() * (252 ** 0.5)
            
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_period = period
        
        return {
            'optimized_parameters': {
                'period': best_period,
                'sharpe_ratio': best_sharpe
            }
        }
    
    return {
        'error': f'Strategy type {strategy_type} not supported for optimization'
    } 