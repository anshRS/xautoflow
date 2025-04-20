import logging
import json
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from sklearn.model_selection import ParameterGrid
from skopt import gp_minimize
from skopt.space import Real, Integer, Categorical

logger = logging.getLogger(__name__)

def fetch_historical_data(ticker: str, period: str = "1y", interval: str = "1d") -> Dict[str, Any]:
    """Fetch historical price data for a ticker symbol.
    
    Args:
        ticker: The ticker symbol (e.g., "AAPL")
        period: Time period (e.g., "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
        interval: Data interval (e.g., "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
    
    Returns:
        Dictionary with historical price data
    """
    # In a production environment, you would integrate with a real market data API
    # such as yfinance, Alpha Vantage, IEX Cloud, etc.
    # This is simulated data for development/demonstration
    
    logger.info(f"Fetching historical data: {ticker}, period={period}, interval={interval}")
    
    try:
        # Define date range
        end_date = datetime.now()
        
        if period == "1d":
            start_date = end_date - timedelta(days=1)
            num_points = 24
        elif period == "5d":
            start_date = end_date - timedelta(days=5)
            num_points = 5
        elif period == "1mo":
            start_date = end_date - timedelta(days=30)
            num_points = 30
        elif period == "3mo":
            start_date = end_date - timedelta(days=90)
            num_points = 90
        elif period == "6mo":
            start_date = end_date - timedelta(days=180)
            num_points = 180
        elif period == "1y":
            start_date = end_date - timedelta(days=365)
            num_points = 252  # Approximate trading days in a year
        elif period == "2y":
            start_date = end_date - timedelta(days=365*2)
            num_points = 252*2
        elif period == "5y":
            start_date = end_date - timedelta(days=365*5)
            num_points = 252*5
        else:
            start_date = end_date - timedelta(days=365)
            num_points = 252
            
        # Generate simulated price data
        # Start with a reasonable price for the stock (this would be replaced with real data)
        if ticker in ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]:
            # Simulate tech stock prices
            base_price = 150.0
            volatility = 0.015
        elif ticker in ["JPM", "BAC", "WFC", "C", "GS"]:
            # Simulate financial stock prices
            base_price = 80.0
            volatility = 0.01
        elif ticker in ["XOM", "CVX", "BP", "RDS-A", "TOT"]:
            # Simulate energy stock prices
            base_price = 60.0
            volatility = 0.02
        else:
            # Default simulation
            base_price = 100.0
            volatility = 0.012
            
        # Generate time series
        date_range = pd.date_range(start=start_date, end=end_date, periods=num_points)
        
        # Generate simulated price series with a random walk and slight upward bias
        np.random.seed(hash(ticker) % 10000)  # Use ticker as seed for consistent but different results
        returns = np.random.normal(0.0002, volatility, num_points)  # Slight positive bias
        price_series = base_price * (1 + np.cumsum(returns))
        
        # Create OHLC data with some variation
        data = []
        for i in range(num_points):
            date = date_range[i]
            close = price_series[i]
            
            # Simulate intraday volatility
            daily_volatility = close * volatility * 0.5
            high = close + abs(np.random.normal(0, daily_volatility))
            low = close - abs(np.random.normal(0, daily_volatility))
            # Ensure low is less than high
            if low > high:
                low, high = high, low
                
            # Opening price between previous close and current close
            if i == 0:
                open_price = close - np.random.normal(0, daily_volatility)
            else:
                prev_close = price_series[i-1]
                open_price = prev_close + np.random.normal(0, daily_volatility)
                
            # Ensure open is between high and low
            open_price = min(max(open_price, low), high)
            
            # Trading volume - simulated with some randomness
            volume = int(np.random.normal(1000000, 300000))
            
            data.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "open": round(float(open_price), 2),
                "high": round(float(high), 2),
                "low": round(float(low), 2),
                "close": round(float(close), 2),
                "volume": max(0, volume)
            })
        
        return {
            "ticker": ticker,
            "period": period,
            "interval": interval,
            "data": data,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}: {e}", exc_info=True)
        return {
            "ticker": ticker,
            "status": "error",
            "error": str(e)
        }

def calculate_technical_indicators(data: Union[Dict[str, Any], str], indicators: List[str]) -> Dict[str, Any]:
    """Calculate technical indicators for a price dataset.
    
    Args:
        data: Price data dictionary or DataFrame as JSON string
        indicators: List of indicators to calculate, e.g., ["sma", "ema", "rsi", "macd", "bollinger_bands"]
    
    Returns:
        Dictionary with calculated indicators
    """
    logger.info(f"Calculating indicators: {', '.join(indicators)}")
    
    try:
        # Parse data if provided as JSON string
        if isinstance(data, str):
            data = json.loads(data)
            
        # If data is a dictionary from fetch_historical_data, extract the price data array
        if isinstance(data, dict) and "data" in data:
            price_data = data["data"]
        else:
            price_data = data
            
        # Convert to pandas DataFrame for easier calculation
        df = pd.DataFrame(price_data)
        
        # Ensure date column is datetime
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            
        # Initialize results dictionary
        results = {
            "status": "success",
            "indicators": {}
        }
        
        # Calculate requested indicators
        for indicator in indicators:
            indicator = indicator.lower()
            
            if indicator == "sma" or indicator.startswith("sma_"):
                # Extract period from indicator name (e.g., "sma_20" -> 20)
                if indicator.startswith("sma_"):
                    period = int(indicator.split("_")[1])
                else:
                    period = 20  # Default period
                
                # Calculate Simple Moving Average
                df[f"sma_{period}"] = df["close"].rolling(window=period).mean()
                results["indicators"][f"sma_{period}"] = df[f"sma_{period}"].dropna().to_dict()
                
            elif indicator == "ema" or indicator.startswith("ema_"):
                # Extract period
                if indicator.startswith("ema_"):
                    period = int(indicator.split("_")[1])
                else:
                    period = 20  # Default period
                
                # Calculate Exponential Moving Average
                df[f"ema_{period}"] = df["close"].ewm(span=period, adjust=False).mean()
                results["indicators"][f"ema_{period}"] = df[f"ema_{period}"].to_dict()
                
            elif indicator == "rsi" or indicator.startswith("rsi_"):
                # Extract period
                if indicator.startswith("rsi_"):
                    period = int(indicator.split("_")[1])
                else:
                    period = 14  # Default period
                
                # Calculate RSI
                delta = df["close"].diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                
                avg_gain = gain.rolling(window=period).mean()
                avg_loss = loss.rolling(window=period).mean()
                
                rs = avg_gain / avg_loss
                df[f"rsi_{period}"] = 100 - (100 / (1 + rs))
                results["indicators"][f"rsi_{period}"] = df[f"rsi_{period}"].dropna().to_dict()
                
            elif indicator == "macd":
                # Calculate MACD (12, 26, 9)
                df["ema_12"] = df["close"].ewm(span=12, adjust=False).mean()
                df["ema_26"] = df["close"].ewm(span=26, adjust=False).mean()
                df["macd_line"] = df["ema_12"] - df["ema_26"]
                df["macd_signal"] = df["macd_line"].ewm(span=9, adjust=False).mean()
                df["macd_histogram"] = df["macd_line"] - df["macd_signal"]
                
                results["indicators"]["macd"] = {
                    "macd_line": df["macd_line"].to_dict(),
                    "signal_line": df["macd_signal"].to_dict(),
                    "histogram": df["macd_histogram"].to_dict()
                }
                
            elif indicator == "bollinger_bands" or indicator.startswith("bollinger_"):
                # Extract period and standard deviation
                if indicator.startswith("bollinger_"):
                    parts = indicator.split("_")
                    period = int(parts[1]) if len(parts) > 1 else 20
                    std_dev = float(parts[2]) if len(parts) > 2 else 2.0
                else:
                    period = 20
                    std_dev = 2.0
                
                # Calculate Bollinger Bands
                df[f"sma_{period}"] = df["close"].rolling(window=period).mean()
                df[f"std_{period}"] = df["close"].rolling(window=period).std()
                df[f"bollinger_upper"] = df[f"sma_{period}"] + (df[f"std_{period}"] * std_dev)
                df[f"bollinger_lower"] = df[f"sma_{period}"] - (df[f"std_{period}"] * std_dev)
                
                results["indicators"][f"bollinger_bands_{period}_{std_dev}"] = {
                    "middle_band": df[f"sma_{period}"].dropna().to_dict(),
                    "upper_band": df[f"bollinger_upper"].dropna().to_dict(),
                    "lower_band": df[f"bollinger_lower"].dropna().to_dict()
                }
            
            elif indicator == "atr" or indicator.startswith("atr_"):
                # Extract period
                if indicator.startswith("atr_"):
                    period = int(indicator.split("_")[1])
                else:
                    period = 14  # Default period
                
                # Calculate True Range
                df["high_low"] = df["high"] - df["low"]
                df["high_close"] = abs(df["high"] - df["close"].shift())
                df["low_close"] = abs(df["low"] - df["close"].shift())
                df["tr"] = df[["high_low", "high_close", "low_close"]].max(axis=1)
                
                # Calculate Average True Range
                df[f"atr_{period}"] = df["tr"].rolling(window=period).mean()
                results["indicators"][f"atr_{period}"] = df[f"atr_{period}"].dropna().to_dict()
            
            # Add more indicators as needed...
                
        return results
    
    except Exception as e:
        logger.error(f"Error calculating indicators: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }

def optimize_strategy_parameters(strategy_type: str, parameters_space: Dict[str, Any], 
                                data: Dict[str, Any], optimization_target: str = "sharpe_ratio") -> Dict[str, Any]:
    """Find optimal parameters for a trading strategy using historical data.
    
    Args:
        strategy_type: Type of strategy to optimize (e.g., "moving_average_crossover", "rsi", "macd")
        parameters_space: Dictionary of parameter ranges to search
        data: Historical price data for optimization
        optimization_target: Metric to optimize (e.g., "sharpe_ratio", "total_return")
    
    Returns:
        Dictionary with optimized parameters and performance metrics
    """
    logger.info(f"Optimizing {strategy_type} strategy parameters for {optimization_target}")
    
    try:
        # Extract price data
        if isinstance(data, str):
            data = json.loads(data)
            
        if isinstance(data, dict) and "data" in data:
            price_data = data["data"]
        else:
            price_data = data
            
        # Convert to pandas DataFrame
        df = pd.DataFrame(price_data)
        
        # Ensure date column is datetime
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
        
        # Define strategy evaluation function
        def evaluate_strategy(params: Dict[str, Any]) -> float:
            """Evaluate a strategy with given parameters.
            
            Args:
                params: Strategy parameters
                
            Returns:
                Performance metric (negative for minimization)
            """
            # Implementation depends on strategy_type
            if strategy_type == "moving_average_crossover":
                short_window = params["short_window"]
                long_window = params["long_window"]
                
                # Calculate MAs
                df[f"sma_{short_window}"] = df["close"].rolling(window=short_window).mean()
                df[f"sma_{long_window}"] = df["close"].rolling(window=long_window).mean()
                
                # Generate signals
                df["signal"] = 0
                df["signal"][long_window:] = np.where(
                    df[f"sma_{short_window}"][long_window:] > df[f"sma_{long_window}"][long_window:], 1, 0
                )
                
                # Calculate position changes
                df["position"] = df["signal"].diff()
                
            elif strategy_type == "rsi":
                rsi_period = params["rsi_period"]
                oversold = params["oversold"]
                overbought = params["overbought"]
                
                # Calculate RSI
                delta = df["close"].diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                
                avg_gain = gain.rolling(window=rsi_period).mean()
                avg_loss = loss.rolling(window=rsi_period).mean()
                
                rs = avg_gain / avg_loss
                df["rsi"] = 100 - (100 / (1 + rs))
                
                # Generate signals: buy when RSI < oversold, sell when RSI > overbought
                df["signal"] = 0
                df.loc[df["rsi"] < oversold, "signal"] = 1
                df.loc[df["rsi"] > overbought, "signal"] = 0
                
                # Calculate position changes
                df["position"] = df["signal"].diff()
                
            elif strategy_type == "macd":
                fast_period = params["fast_period"]
                slow_period = params["slow_period"]
                signal_period = params["signal_period"]
                
                # Calculate MACD
                df["ema_fast"] = df["close"].ewm(span=fast_period, adjust=False).mean()
                df["ema_slow"] = df["close"].ewm(span=slow_period, adjust=False).mean()
                df["macd_line"] = df["ema_fast"] - df["ema_slow"]
                df["macd_signal"] = df["macd_line"].ewm(span=signal_period, adjust=False).mean()
                
                # Generate signals: buy when MACD crosses above signal, sell when crosses below
                df["signal"] = 0
                df["signal"] = np.where(df["macd_line"] > df["macd_signal"], 1, 0)
                
                # Calculate position changes
                df["position"] = df["signal"].diff()
            
            # Simulate trades and calculate returns
            df["position"] = df["position"].fillna(0)
            df["returns"] = df["close"].pct_change()
            df["strategy_returns"] = df["position"].shift() * df["returns"]
            
            # Drop NaN values
            valid_data = df.dropna()
            
            if len(valid_data) < 10:  # Need enough data for meaningful evaluation
                return -999999  # Large negative value for minimization
                
            # Calculate performance metrics
            total_return = (1 + valid_data["strategy_returns"]).prod() - 1
            
            # Annualized return (assuming 252 trading days)
            n_periods = len(valid_data)
            ann_factor = 252 / n_periods
            ann_return = (1 + total_return) ** ann_factor - 1
            
            # Annualized volatility
            ann_vol = valid_data["strategy_returns"].std() * np.sqrt(252)
            
            # Sharpe ratio (using 0 as risk-free rate for simplicity)
            sharpe_ratio = ann_return / ann_vol if ann_vol > 0 else 0
            
            # Maximum drawdown
            cum_returns = (1 + valid_data["strategy_returns"]).cumprod()
            max_dd = (cum_returns / cum_returns.cummax() - 1).min()
            
            # Return the negative of the target metric for minimization
            if optimization_target == "sharpe_ratio":
                return -sharpe_ratio
            elif optimization_target == "total_return":
                return -total_return
            elif optimization_target == "drawdown":
                return max_dd
            else:
                return -sharpe_ratio
        
        # Optimization approach depends on parameter space
        results = {}
        
        # Grid search for small parameter spaces
        if all(isinstance(v, (list, tuple)) for v in parameters_space.values()):
            param_grid = list(ParameterGrid(parameters_space))
            
            if len(param_grid) <= 100:  # Only use grid search for reasonable size
                logger.info(f"Using grid search for {len(param_grid)} parameter combinations")
                
                best_score = float('inf')
                best_params = None
                
                for params in param_grid:
                    score = evaluate_strategy(params)
                    
                    if score < best_score:
                        best_score = score
                        best_params = params
                
                # Best parameters
                results["best_parameters"] = best_params
                results["optimization_method"] = "grid_search"
            else:
                logger.info("Parameter space too large for grid search, using Bayesian optimization")
                # Fall through to Bayesian optimization
                
        # Bayesian optimization for larger or continuous parameter spaces
        if "best_parameters" not in results:
            # Define search space for skopt
            space = []
            param_names = []
            
            for param, value in parameters_space.items():
                param_names.append(param)
                
                if isinstance(value, list):
                    # Categorical or discrete parameter
                    space.append(Categorical(value, name=param))
                elif isinstance(value, dict) and all(k in value for k in ["min", "max"]):
                    # Continuous parameter range
                    if value.get("type", "float") == "int":
                        space.append(Integer(value["min"], value["max"], name=param))
                    else:
                        space.append(Real(value["min"], value["max"], name=param))
            
            # Wrapper function to convert list of parameter values to dictionary
            def objective(x):
                params = dict(zip(param_names, x))
                return evaluate_strategy(params)
            
            # Run Bayesian optimization
            logger.info("Running Bayesian optimization")
            res_gp = gp_minimize(objective, space, n_calls=50, random_state=42)
            
            # Extract best parameters
            best_params = dict(zip(param_names, res_gp.x))
            results["best_parameters"] = best_params
            results["optimization_method"] = "bayesian_optimization"
        
        # Evaluate best parameters to get performance metrics
        best_params = results["best_parameters"]
        
        # Re-evaluate the strategy with best parameters to get metrics
        # (Using negative of the evaluation function result)
        if strategy_type == "moving_average_crossover":
            short_window = best_params["short_window"]
            long_window = best_params["long_window"]
            
            df[f"sma_{short_window}"] = df["close"].rolling(window=short_window).mean()
            df[f"sma_{long_window}"] = df["close"].rolling(window=long_window).mean()
            
            df["signal"] = 0
            df["signal"][long_window:] = np.where(
                df[f"sma_{short_window}"][long_window:] > df[f"sma_{long_window}"][long_window:], 1, 0
            )
            
        elif strategy_type == "rsi":
            rsi_period = best_params["rsi_period"]
            oversold = best_params["oversold"]
            overbought = best_params["overbought"]
            
            delta = df["close"].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=rsi_period).mean()
            avg_loss = loss.rolling(window=rsi_period).mean()
            
            rs = avg_gain / avg_loss
            df["rsi"] = 100 - (100 / (1 + rs))
            
            df["signal"] = 0
            df.loc[df["rsi"] < oversold, "signal"] = 1
            df.loc[df["rsi"] > overbought, "signal"] = 0
            
        elif strategy_type == "macd":
            fast_period = best_params["fast_period"]
            slow_period = best_params["slow_period"]
            signal_period = best_params["signal_period"]
            
            df["ema_fast"] = df["close"].ewm(span=fast_period, adjust=False).mean()
            df["ema_slow"] = df["close"].ewm(span=slow_period, adjust=False).mean()
            df["macd_line"] = df["ema_fast"] - df["ema_slow"]
            df["macd_signal"] = df["macd_line"].ewm(span=signal_period, adjust=False).mean()
            
            df["signal"] = 0
            df["signal"] = np.where(df["macd_line"] > df["macd_signal"], 1, 0)
        
        # Calculate position changes and returns
        df["position"] = df["signal"].diff().fillna(0)
        df["returns"] = df["close"].pct_change()
        df["strategy_returns"] = df["position"].shift() * df["returns"]
        
        # Performance metrics on cleaned data
        valid_data = df.dropna()
        
        # Calculate performance metrics
        total_return = (1 + valid_data["strategy_returns"]).prod() - 1
        
        # Annualized return (assuming 252 trading days)
        n_periods = len(valid_data)
        ann_factor = 252 / n_periods
        ann_return = (1 + total_return) ** ann_factor - 1
        
        # Annualized volatility
        ann_vol = valid_data["strategy_returns"].std() * np.sqrt(252)
        
        # Sharpe ratio (using 0 as risk-free rate for simplicity)
        sharpe_ratio = ann_return / ann_vol if ann_vol > 0 else 0
        
        # Maximum drawdown
        cum_returns = (1 + valid_data["strategy_returns"]).cumprod()
        max_dd = (cum_returns / cum_returns.cummax() - 1).min()
        
        # Win rate (percentage of winning trades)
        trade_returns = valid_data.loc[valid_data["position"] != 0, "strategy_returns"]
        win_rate = (trade_returns > 0).sum() / len(trade_returns) if len(trade_returns) > 0 else 0
        
        # Add performance metrics to results
        results["performance_metrics"] = {
            "total_return": float(total_return),
            "annualized_return": float(ann_return),
            "annualized_volatility": float(ann_vol),
            "sharpe_ratio": float(sharpe_ratio),
            "max_drawdown": float(max_dd),
            "win_rate": float(win_rate)
        }
        
        results["status"] = "success"
        
        return results
    
    except Exception as e:
        logger.error(f"Error optimizing strategy parameters: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        } 