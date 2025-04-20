from typing import Dict, Any
import pandas as pd
import vectorbt as vbt

def run_vectorbt_backtest(
    data_dict: Dict[str, Any],
    strategy_params: dict,
    logic_identifier: str
) -> Dict[str, Any]:
    try:
        # Convert data to DataFrame
        df = pd.DataFrame(data_dict['data'])
        df.set_index('date', inplace=True)
        
        # Generate signals based on logic identifier
        if logic_identifier == "moving_average_crossover":
            fast_ma = vbt.MA.run(df.close, window=strategy_params['fast_period'])
            slow_ma = vbt.MA.run(df.close, window=strategy_params['slow_period'])
            entries = fast_ma.ma_above(slow_ma)
            exits = fast_ma.ma_below(slow_ma)
            
        elif logic_identifier == "rsi_reversal":
            rsi = vbt.RSI.run(df.close, window=strategy_params['rsi_period'])
            entries = rsi.rsi_below(strategy_params['oversold_threshold'])
            exits = rsi.rsi_above(strategy_params['overbought_threshold'])
        
        else:
            raise ValueError(f"Unknown strategy logic: {logic_identifier}")
        
        # Run backtest
        portfolio = vbt.Portfolio.from_signals(
            df.close,
            entries,
            exits,
            init_cash=strategy_params.get('initial_capital', 100000),
            fees=strategy_params.get('transaction_fee', 0.001)
        )
        
        # Calculate metrics
        metrics = portfolio.stats()
        
        return {
            "success": True,
            "metrics": {
                "total_return": metrics['Total Return [%]'],
                "sharpe_ratio": metrics['Sharpe Ratio'],
                "max_drawdown": metrics['Max Drawdown [%]'],
                "win_rate": metrics['Win Rate [%]'],
                "profit_factor": metrics['Profit Factor']
            },
            "trades": portfolio.trades.records_readable
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }