# Monte Carlo Portfolio Simulation & Efficient Frontier Analysis

## Overview

This project is a **Monte Carlo portfolio simulation built in Python** to explore the relationship between portfolio return, volatility, and the Sharpe ratio.

I started this project after working on stock-level analysis and wanted to take the next step:

> **What happens when I combine several stocks into a portfolio and test thousands of different allocations?**

Instead of manually testing a few portfolio combinations, I generated **5,000 random portfolio allocations** and calculated the expected return, volatility, Sharpe ratio, final portfolio value, and return on investment for each one.

The final output is a risk-return visualization showing how the simulated portfolios are distributed and highlighting the portfolio with the **highest simulated Sharpe ratio**.

---

## Project Objective

The main objectives of this project are to:

- Build a diversified portfolio from multiple stocks.
- Generate random portfolio weights.
- Calculate portfolio expected return.
- Calculate portfolio volatility using the covariance matrix.
- Calculate the Sharpe ratio.
- Calculate final portfolio value and historical return on investment.
- Run 5,000 Monte Carlo simulations.
- Visualize the simulated risk-return combinations.
- Identify the simulated portfolio with the highest Sharpe ratio.

This project is primarily an **educational and exploratory portfolio-analysis project** rather than a stock-price forecasting model.

---

# Why I Built This

My previous stock-analysis work focused on understanding individual stocks through:

- Closing prices
- Trading volume
- Daily returns
- Moving averages
- Correlation
- Return distributions

The natural next question was:

**"How do these individual stocks behave when they are combined into a portfolio?"**

That is where portfolio theory becomes more interesting.

A portfolio's behaviour depends on much more than the return of each individual stock. It also depends on:

**Portfolio Weights + Individual Returns + Volatility + Correlation/Covariance**

Monte Carlo simulation gave me a practical way to experiment with thousands of different allocations and see how these factors affect the overall portfolio.

---

# Project Structure

The repository is organized as follows:

```text
Monte_Carlo_Simulation_Tata-Elxsi/
│
├── Efficient_Fronter/
│   ├── Monte_Carlo_Risk_Return.png
│   ├── Monte_Carlo_efficient_frontier.png
│   ├── Monte Carlo Simulation.py
│   └── Monte_Carlo_Simulations.ipynb
│
└── README.md
```

### File description

**`Efficient_Fronter/Monte Carlo Simulation.py`**  
Contains the Python workflow for portfolio construction, metric calculation, Monte Carlo simulation, and visualization.

**`Efficient_Fronter/Monte_Carlo_Simulations.ipynb`**  
Notebook version of the Monte Carlo portfolio analysis.

**`Efficient_Fronter/Monte_Carlo_Risk_Return.png`**  
Risk-return scatter plot containing the simulated portfolios.

**`Efficient_Fronter/Monte_Carlo_efficient_frontier.png`**  
Risk-return visualization with the highest-Sharpe simulated portfolio highlighted.

> The chart files are stored inside the `Efficient_Fronter` folder. The image links below use the repository's raw GitHub paths so that the plots render directly inside the README.

---

# My Approach

I followed the analysis in a logical sequence.

## 1. Load the Stock Dataset

The project starts by loading the diversified stock dataset:

```python
raw_df = pd.read_csv('Diversified_stocks.csv')
```

The data is then copied for portfolio calculations.

The script expects the CSV file to be available in the working directory when the code is run.

---

## 2. Scale the Prices

The stocks have different starting price levels, so comparing their raw prices directly would not be very meaningful.

I created a `price_scaling()` function that divides every stock's price by its first available price:

```text
Scaled Price = Current Price / Initial Price
```

For example:

```text
Initial Price = 100
Current Price = 125

Scaled Price = 125 / 100
             = 1.25
```

This puts different stocks on a common base and helps compare relative performance.

### What I learned

A higher share price does not automatically mean better performance.

**Normalization allows me to compare growth relative to the starting point.**

---

# 3. Generate Portfolio Weights

The next step was to decide how much of the portfolio should be invested in each stock.

Instead of manually choosing a single allocation, I created a function that generates random weights.

The process is:

1. Generate a random value for every stock.
2. Add all values together.
3. Divide each value by the total.
4. This makes the portfolio weights sum to 1.

Conceptually:

```text
Weightᵢ = Random Valueᵢ / Total Random Value
```

Therefore:

```text
Σ Portfolio Weights = 100%
```

This creates a valid long-only allocation for each simulation.

---

# 4. Allocate the Initial Investment

The model uses:

**Initial Investment = INR 1,000,000**

The allocation process combines scaled stock prices, portfolio weights, and the initial investment.

Conceptually:

```text
Position Value
=
Scaled Price × Portfolio Weight × Initial Investment
```

The individual positions are then added together to obtain the portfolio value.

The model also calculates portfolio daily return as:

```text
Portfolio Daily Return
=
(Current Portfolio Value / Previous Portfolio Value - 1) × 100
```

---

# 5. Calculate Portfolio Return

The model calculates the expected annual portfolio return using the historical average daily return of each stock and the portfolio weights.

The code annualizes the result using **252 trading days**.

Conceptually:

```text
Expected Annual Portfolio Return
=
Σ (Weight × Average Daily Asset Return) × 252
```

This provides an annualized estimate based on the historical data in the dataset.

---

# 6. Calculate Portfolio Volatility

Portfolio volatility is calculated using the covariance matrix of stock returns.

The covariance matrix is annualized using 252 trading days:

```text
Annualized Covariance Matrix
=
Daily Covariance Matrix × 252
```

Portfolio volatility is then calculated using:

```text
Portfolio Volatility
=
√(wᵀΣw)
```

where:

- `w` = vector of portfolio weights
- `Σ` = annualized covariance matrix

### What I learned

Portfolio risk is not simply the weighted average of each stock's individual volatility.

The way stocks move relative to one another matters.

That is why **covariance and correlation are central to portfolio diversification**.

---

# 7. Calculate the Sharpe Ratio

The model uses the Sharpe ratio to evaluate risk-adjusted portfolio performance.

The code assumes a:

**Risk-Free Rate = 7%**

The formula is:

```text
Sharpe Ratio
=
(Expected Portfolio Return - Risk-Free Rate)
/
Portfolio Volatility
```

The Sharpe ratio allows the simulation to compare portfolios with different combinations of return and risk.

A portfolio with a higher expected return is not automatically better from a risk-adjusted perspective if it also has significantly higher volatility.

---

# 8. Calculate Return on Investment

The project also calculates the historical return on the initial investment.

The formula is:

```text
ROI
=
(Final Portfolio Value - Initial Portfolio Value)
/
Initial Portfolio Value
× 100
```

For example, if:

```text
Initial Investment = ₹1,000,000
Final Value = ₹1,200,000
```

then:

```text
ROI = 20%
```

This makes the simulation easier to connect with an actual investment amount.

---

# 9. Run 5,000 Monte Carlo Simulations

The core of the project is the Monte Carlo simulation.

I ran:

**5,000 simulations**

For each simulation:

```text
1. Generate random portfolio weights
2. Allocate the portfolio
3. Calculate expected annual return
4. Calculate annualized volatility
5. Calculate Sharpe ratio
6. Calculate final portfolio value
7. Calculate return on investment
8. Store the results
```

The results are stored in a dataframe containing:

- Volatility
- Portfolio Return
- Sharpe Ratio

This produces thousands of different possible portfolio outcomes.

---

# 10. Identify the Highest-Sharpe Portfolio

After completing all 5,000 simulations, I find the simulation with the maximum Sharpe ratio.

The corresponding weights are then used to calculate the portfolio metrics again.

The resulting output includes:

- Expected annual portfolio return
- Portfolio volatility
- Sharpe ratio
- Final portfolio value
- Return on investment

### Important interpretation

The selected portfolio is:

> **The highest-Sharpe portfolio found among the 5,000 randomly generated portfolios.**

It is not proof that this allocation is the mathematical global optimum.

A different random seed, more simulations, or a constrained optimization algorithm could produce a different allocation.

---

# Risk-Return Visualizations

## 1. Monte Carlo Risk-Return Plot

Each point represents **one simulated portfolio**.

The chart uses:

- **X-axis → Volatility**
- **Y-axis → Portfolio Return**
- **Colour → Sharpe Ratio**
- **Point Size → Sharpe Ratio**

This creates a visual map of the different risk-return combinations generated during the simulation.

### What the chart shows

The portfolio points form a broad cloud rather than a single line.

This happens because changing the portfolio weights changes the resulting return, volatility, and Sharpe ratio.

The upper portion of the cloud contains portfolios with relatively higher expected returns, while the lower portion contains portfolios with lower expected returns.

### Visualization

![Monte Carlo Risk-Return Plot](https://raw.githubusercontent.com/ayantikpandit/Monte_Carlo_Simulation_Tata-Elxsi/main/Efficient_Frontier/Monte_Carlo_Risk_Return.png)

---

## 2. Monte Carlo Efficient Frontier / Highlighted Portfolio

The second chart uses the same risk-return information but adds a highlighted point for the portfolio with the maximum simulated Sharpe ratio.

### Visualization

![Monte Carlo Efficient Frontier](https://raw.githubusercontent.com/ayantikpandit/Monte_Carlo_Simulation_Tata-Elxsi/main/Efficient_Frontier/Monte_Carlo_efficient_frontier.png)

The highlighted point represents the allocation that produced the highest Sharpe ratio **within the 5,000 simulated portfolios**.

### Important distinction

This visualization is useful for understanding the simulated risk-return opportunity set.

However, because the portfolios are generated using random weights, the chart should not automatically be treated as a mathematically complete efficient frontier.

A formal efficient frontier would normally be constructed using an optimization procedure across different target return or risk levels.

---

# Analysis & Key Observations

## 1. Portfolio allocation changes the outcome

The simulation demonstrates that using the same group of stocks does not mean every portfolio behaves the same way.

Changing the weights can change:

- Expected return
- Volatility
- Sharpe ratio
- Final portfolio value

### Takeaway

**Asset selection matters, but asset allocation matters too.**

---

## 2. Higher expected return generally comes with higher volatility

The simulated portfolios show an upward relationship between expected return and volatility.

This reflects the risk-return trade-off present in the historical data used by the model.

### Takeaway

It is not enough to ask:

**"Which portfolio has the highest return?"**

I also need to ask:

**"How much risk am I taking to achieve that return?"**

---

## 3. Sharpe ratio helps compare risk-adjusted performance

A portfolio with a high return may also have very high volatility.

Another portfolio may produce a slightly lower return with significantly lower volatility.

The Sharpe ratio captures this trade-off by comparing excess return with volatility.

### Takeaway

Looking at return alone gives only part of the picture.

---

## 4. Diversification depends on relationships between assets

The volatility calculation uses the covariance matrix.

This means the portfolio's risk depends on how the stocks move together.

Two assets can have similar individual volatility but still produce different portfolio outcomes depending on their covariance with the rest of the portfolio.

### Takeaway

**Diversification is about the relationship between assets, not just the number of assets.**

---

## 5. The highest-return portfolio and highest-Sharpe portfolio can be different

This is one of the most useful concepts demonstrated by the simulation.

A portfolio can achieve a very high expected return but take on a disproportionately high level of volatility.

Another portfolio may generate a lower expected return but provide better risk-adjusted performance.

The simulation therefore highlights the difference between:

```text
Maximum Return
```

and

```text
Maximum Risk-Adjusted Return
```

---

## 6. The highlighted portfolio depends on the simulation

Because the portfolio weights are randomly generated, the maximum-Sharpe portfolio depends on which allocations were sampled.

Running the simulation again can result in different:

- Portfolio weights
- Returns
- Volatility
- Sharpe ratios

### Takeaway

Monte Carlo simulation is an approximation based on sampled scenarios.

The more scenarios we generate, the more extensively we explore the possible weight combinations, but randomness still plays a role unless the simulation is controlled by a fixed seed.

---

# What I Learned From This Project

This project helped me connect financial theory with actual coding and data analysis.

## 1. Portfolio theory became practical

Concepts such as:

- Covariance
- Volatility
- Diversification
- Sharpe ratio
- Portfolio weights

became much easier to understand once I implemented them in code.

---

## 2. Weight allocation is extremely important

Two portfolios can contain exactly the same stocks but produce very different outcomes because the allocation percentages are different.

This made portfolio construction much more intuitive for me.

---

## 3. Risk depends on more than individual stocks

Portfolio risk is influenced by the interactions between assets.

That is why covariance is necessary when calculating total portfolio volatility.

---

## 4. Simulation is useful for exploring many possibilities

With multiple assets, there are countless possible combinations of portfolio weights.

Testing a few manually would not be enough to understand the full range of outcomes.

Monte Carlo simulation provides a practical way to explore thousands of possibilities quickly.

---

## 5. Visualization makes quantitative finance easier to understand

The simulation generates thousands of numerical results.

The risk-return scatter plot turns those results into something much easier to interpret visually.

Instead of looking through thousands of rows, I can see the overall distribution of portfolio outcomes in one chart.

---

## 6. "Optimal" always depends on the objective

This was one of the most important lessons for me.

A portfolio can be considered optimal according to different objectives:

- Maximum return
- Minimum volatility
- Maximum Sharpe ratio
- Minimum drawdown
- A target return
- A target level of risk

In this project, the objective is specifically:

**Maximum Sharpe ratio among the simulated portfolios.**

That definition matters.

---

# Technical Concepts Covered

This project gave me hands-on experience with:

### Portfolio Construction
Combining multiple stocks using portfolio weights.

### Price Scaling
Normalizing stock-price series to a common starting point.

### Daily Returns
Calculating percentage changes between observations.

### Annualization
Using 252 trading days to annualize daily return and covariance statistics.

### Covariance Matrix
Measuring how asset returns move together.

### Portfolio Volatility
Calculating overall portfolio risk using:

```text
√(wᵀΣw)
```

### Sharpe Ratio
Comparing portfolio excess return with portfolio volatility.

### Monte Carlo Simulation
Generating many random portfolio allocations and comparing their results.

### Risk-Return Analysis
Visualizing the relationship between portfolio expected return and volatility.

---

# Limitations

Like any financial model, this project depends on assumptions.

## Historical Data

The analysis uses historical stock-price data.

Historical behaviour does not guarantee future results.

---

## Historical Average Return

The expected return is based on historical average daily returns.

This is an assumption used by the model rather than a prediction of actual future performance.

---

## Risk-Free Rate

The model assumes a fixed risk-free rate of **7%**.

Changing this assumption changes the Sharpe ratio calculations.

---

## 252 Trading Days

The model annualizes daily values using 252 trading days, which is a standard market convention.

---

## Random Portfolio Weights

Only 5,000 random portfolios are tested.

The model therefore samples the possible allocation space rather than exhaustively searching every possible combination.

---

## No Transaction Costs

The current model does not include:

- Brokerage charges
- Taxes
- Slippage
- Bid-ask spreads
- Rebalancing costs

---

## No Portfolio Constraints

The simulation does not currently impose constraints such as:

- Maximum allocation to one stock
- Sector limits
- Turnover limits
- Liquidity restrictions
- Short-selling restrictions

---

## No Future Price Forecast

This project is not a stock-price prediction model.

It uses historical return and covariance information to evaluate different portfolio allocations.

---

# Future Improvements

I would like to take this project further by adding:

## 1. Mean-Variance Optimization

Use an optimization algorithm to calculate:

- Minimum-variance portfolio
- Maximum-Sharpe portfolio
- Target-return portfolios

This would provide a more rigorous efficient frontier.

---

## 2. Portfolio Constraints

Introduce practical constraints such as:

```text
Minimum Weight = 0%
Maximum Weight = 20%
```

This would make the simulated portfolios more realistic.

---

## 3. Benchmark Comparison

Compare portfolio performance against a benchmark such as a relevant market index.

---

## 4. Maximum Drawdown

Add maximum drawdown to understand the severity of historical portfolio declines.

---

## 5. Rolling Metrics

Add:

- Rolling volatility
- Rolling Sharpe ratio
- Rolling correlation
- Rolling beta

This would help show how portfolio risk changes through time.

---

## 6. More Advanced Monte Carlo Simulation

A future version could simulate future return paths rather than only generating random portfolio weights.

Possible methods include:

- Historical bootstrapping
- Correlated random returns
- Geometric Brownian Motion
- Other stochastic models

---

## 7. Build an Interactive Portfolio Dashboard

The simulation could eventually be turned into an interactive dashboard where users can change:

- Number of simulations
- Initial investment
- Risk-free rate
- Portfolio constraints
- Stock selection

and immediately see how the portfolio results change.

---

# How to Run the Project

## 1. Clone the repository

```bash
git clone https://github.com/ayantikpandit/Monte_Carlo_Simulation_Tata-Elxsi.git
cd Monte_Carlo_Simulation_Tata-Elxsi
```

## 2. Install the required libraries

```bash
pip install pandas numpy yfinance seaborn plotly matplotlib
```

## 3. Make sure the dataset is available

The Python script expects:

```text
Diversified_stocks.csv
```

The code loads it using:

```python
raw_df = pd.read_csv('Diversified_stocks.csv')
```

So keep the CSV in the location expected by the script when running the project locally.

## 4. Run the Python script

```bash
python "Efficient_Fronter/Monte Carlo Simulation.py"
```

## 5. Open the notebook version

You can also open:

```text
Efficient_Fronter/Monte_Carlo_Simulations.ipynb
```

in Jupyter Notebook or VS Code.

---

# A Note About the Code

The project was developed iteratively, so some setup and compatibility steps are included in the script.

The workflow contains package installation/reinstallation steps for Plotly and uses helper functions for:

- Price scaling
- Weight generation
- Asset allocation
- Portfolio metric calculation
- Financial-data plotting

When reproducing the analysis, it is best to execute the workflow in the intended sequence so that helper functions are defined before they are used.

---

# Final Takeaway

I started this project with a simple question:

**"What can I learn by testing thousands of different portfolio allocations instead of manually choosing one?"**

The Monte Carlo simulation helped me see portfolio theory in a much more practical way.

The biggest lesson for me was that portfolio analysis is not only about finding stocks with high returns. It is about understanding the interaction between:

**Return + Risk + Covariance + Portfolio Weights**

This project helped me turn concepts such as **diversification, covariance, volatility, Sharpe ratio, and efficient-frontier analysis** from formulas into something I could actually build, test, and visualize.

It also gave me practical experience in using Python for financial analysis and helped me understand how quantitative methods can support portfolio decision-making.

For me, this project was a step from **individual stock analysis toward portfolio management and quantitative finance**.

---

# Disclaimer

This project is intended for **educational and analytical purposes only**.

The simulations are based on historical data and assumptions defined in the code. The results are not investment recommendations and should not be interpreted as guaranteed future performance.

---

# Author

**Ayantik Pandit**

Finance Student | Financial Analysis | Python | Data Visualization | Portfolio Analysis

### Connect with me

[LinkedIn – Ayantik Pandit](https://www.linkedin.com/in/ayantik-pandit/)
