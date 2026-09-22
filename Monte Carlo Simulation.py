# %%
%pip install --upgrade plotly pandas

# %%
import pandas as pd 
import numpy as np
import datetime as dt 
import yfinance as yf 
import seaborn as sns 
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random as rd
import plotly.graph_objects as go

# %%
raw_df = pd.read_csv('Diversified_stocks.csv')
raw_df

# %%
portfolio_df = raw_df.copy()
scaled_df = price_scaling(portfolio_df)
scaled_df

# %%
def price_scaling(raw_prices_df):
    scaled_prices_df = raw_prices_df.copy()
    for i in raw_prices_df.columns[1:]:
          scaled_prices_df[i] = raw_prices_df[i]/raw_prices_df[i][0]
    return scaled_prices_df

# %%
scaled_df = price_scaling(raw_df)
scaled_df

# %%
weights = [0.032266, 0.094461, 0.117917, 0.132624, 0.145942, 0.128299, 0.10009, 0.007403, 0.088581, 0.152417]
weights

# %%

def generate_portfolio_weights(n):
    weights = []
    for i in range(n):
        weights.append(rd.random())
        
    weights = weights/np.sum(weights)
    return weights

# %%
weights = generate_portfolio_weights(6)
print(weights)

# %%
def asset_allocation(df, weights, initial_investment):
    portfolio_df = df.copy()
    scaled_df = price_scaling(df)
  
    for i, stock in enumerate(scaled_df.columns[1:]):
        portfolio_df[stock] = scaled_df[stock] * weights[i] * initial_investment
    portfolio_df['Portfolio Value [INR]'] = portfolio_df[portfolio_df != 'Date'].sum(axis = 1, numeric_only = True)
    portfolio_df['Portfolio Daily Return [%]'] = portfolio_df['Portfolio Value [INR]'].pct_change(1) * 100 
    portfolio_df.replace(np.nan, 0, inplace = True)
    
    return portfolio_df

# %%
n = len(raw_df.columns)-1

print('Number of stocks in the portfolio = {}'.format(n))
weights = generate_portfolio_weights(n).round(6)
print('Portfolio weights in order = {}'.format(weights))
portfolio_df = asset_allocation(raw_df, weights, 1000000)
portfolio_df.round(1)


# %%
%pip uninstall plotly -y
%pip install plotly --no-cache-dir

# %%
import plotly

import plotly.express as px


# %%
def plot_financial_data(df, title):
    
    fig = px.line(title = title)
    
    # For loop that plots all stock prices in the pandas dataframe df
    # Note that index starts with 1 because we want to skip the date column
    
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)

    fig.show()

# %%
portfolio_df

# %%
plot_financial_data(portfolio_df[['Date', 'Portfolio Daily Return [%]']], 'Portfolio Percentage Daily Return [%]')

plot_financial_data(portfolio_df.drop(['Portfolio Value [INR]', 'Portfolio Daily Return [%]'], axis = 1), 'Portfolio positions [$]')

plot_financial_data(portfolio_df[['Date', 'Portfolio Value [INR]']], 'Total Portfolio Value [$]')

# %%
def simulation_engine(weights, initial_investment):
    
    portfolio_df = asset_allocation(
        raw_df,
        weights,
        initial_investment
    )
    
    return_on_investment = (
        (portfolio_df['Portfolio Value [INR]'].iloc[-1] -
         portfolio_df['Portfolio Value [INR]'].iloc[0])
        / portfolio_df['Portfolio Value [INR]'].iloc[0]
    ) * 100
    
    # Remove non-stock columns
    portfolio_daily_return_df = portfolio_df.drop(
        columns=[
            'Date',
            'Portfolio Value [INR]',
            'Portfolio Daily Return [%]'
        ]
    )
    
    # Calculate daily returns of individual stocks
    portfolio_daily_return_df = portfolio_daily_return_df.pct_change(1)
    
    # Expected annual portfolio return
    expected_portfolio_return = (
        np.sum(
            weights * portfolio_daily_return_df.mean()
        ) * 252
    )
    
    # Annualized covariance matrix
    covariance = portfolio_daily_return_df.cov() * 252
    
    # Portfolio volatility
    expected_volatility = np.sqrt(
        np.dot(
            weights.T,
            np.dot(covariance, weights)
        )
    )
    
    # Risk-free rate assumption
    rf = 0.07
    
    # Sharpe ratio
    sharpe_ratio = (
        expected_portfolio_return - rf
    ) / expected_volatility
    
    return (
        expected_portfolio_return,
        expected_volatility,
        sharpe_ratio,
        portfolio_df['Portfolio Value [INR]'].iloc[-1],
        return_on_investment
    )

# %%
initial_investment = 1000000
portfolio_metrics = simulation_engine(weights, initial_investment)

# %%
print('Expected Portfolio Annual Return = {:.2f}%'.format(portfolio_metrics[0] * 100))
print('Portfolio Standard Deviation (Volatility) = {:.2f}%'.format(portfolio_metrics[1] * 100))
print('Sharpe Ratio = {:.2f}'.format(portfolio_metrics[2]))
print('Portfolio Final Value = ${:.2f}'.format(portfolio_metrics[3]))
print('Return on Investment = {:.2f}%'.format(portfolio_metrics[4]))

# %%
#MONTE CARLO SIMULATION function for 5000 runs
sim_runs = 5000
initial_investment = 1000000

# Placeholder to store all weights
weights_runs = np.zeros((sim_runs, n))

# Placeholder to store all Sharpe ratios
sharpe_ratio_runs = np.zeros(sim_runs)

# Placeholder to store all expected returns
expected_portfolio_returns_runs = np.zeros(sim_runs)

# Placeholder to store all volatility values
volatility_runs = np.zeros(sim_runs)

# Placeholder to store all returns on investment
return_on_investment_runs = np.zeros(sim_runs)

# Placeholder to store all final portfolio values
final_value_runs = np.zeros(sim_runs)

for i in range(sim_runs):
    # Generate random weights 
    weights = generate_portfolio_weights(n)
    # Store the weights
    weights_runs[i,:] = weights
    
    # Call "simulation_engine" function and store Sharpe ratio, return and volatility
    # Note that asset allocation is performed using the "asset_allocation" function  
    expected_portfolio_returns_runs[i], volatility_runs[i], sharpe_ratio_runs[i], final_value_runs[i], return_on_investment_runs[i] = simulation_engine(weights, initial_investment)
    print("Simulation Run = {}".format(i))   
    print("Weights = {}, Final Value = ${:.2f}, Sharpe Ratio = {:.2f}".format(weights_runs[i].round(3), final_value_runs[i], sharpe_ratio_runs[i]))   
    print('\n')

# %%
sharpe_ratio_runs

# %%
sharpe_ratio_runs.argmax()

# %%
sharpe_ratio_runs.max()

# %%
weights_runs[sharpe_ratio_runs.argmax(), :]

# %%
# Return Sharpe ratio, volatility corresponding to the best weights allocation (maximum Sharpe ratio)
optimal_portfolio_return, optimal_volatility, optimal_sharpe_ratio, highest_final_value, optimal_return_on_investment = simulation_engine(weights_runs[sharpe_ratio_runs.argmax(), :], initial_investment)
print('Best Portfolio Metrics Based on {} Monte Carlo Simulation Runs:'.format(sim_runs))
print('  - Portfolio Expected Annual Return = {:.02f}%'.format(optimal_portfolio_return * 100))
print('  - Portfolio Standard Deviation (Volatility) = {:.02f}%'.format(optimal_volatility * 100))
print('  - Sharpe Ratio = {:.02f}'.format(optimal_sharpe_ratio))
print('  - Final Value = INR {:.02f}'.format(highest_final_value))
print('  - Return on Investment = {:.02f}%'.format(optimal_return_on_investment))

# %%
sim_out_df = pd.DataFrame({'Volatility': volatility_runs.tolist(), 'Portfolio_Return': expected_portfolio_returns_runs.tolist(), 'Sharpe_Ratio': sharpe_ratio_runs.tolist() })
sim_out_df

# %%
# Plot volatility vs. return for all simulation runs
# Highlight the volatility and return that corresponds to the highest Sharpe ratio
import plotly.graph_objects as go
fig = px.scatter(sim_out_df, x = 'Volatility', y = 'Portfolio_Return', color = 'Sharpe_Ratio', size = 'Sharpe_Ratio', hover_data = ['Sharpe_Ratio'] )
fig.update_layout({'plot_bgcolor': "white"})
fig.show()


# %%
# Let's highlight the point with the highest Sharpe ratio
fig = px.scatter(sim_out_df, x = 'Volatility', y = 'Portfolio_Return', color = 'Sharpe_Ratio', size = 'Sharpe_Ratio', hover_data = ['Sharpe_Ratio'] )
fig.add_trace(go.Scatter(x = [optimal_volatility], y = [optimal_portfolio_return], mode = 'markers', name = 'Optimal Point', marker = dict(size=[40], color = 'red')))
fig.update_layout(coloraxis_colorbar = dict(y = 0.7, dtick = 5))
fig.update_layout({'plot_bgcolor': "white"})
fig.show()


