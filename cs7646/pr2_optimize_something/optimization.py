"""MC1-P2: Optimize a portfolio.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---
Student Name: Sebastian De la Paz
GT User ID: cdelpaz3
GT ID: 902770611
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo


def save_plot(df, filename, title="Stock prices", xlabel="Date", ylabel="Price"):
    import matplotlib.pyplot as plt
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(filename)

def get_portfolio_statistics(prices, yearly_samples=252, risk_free_return=0):
    daily_returns = prices / prices.shift(1) - 1
    cumulative_return = prices[-1] / prices[0] - 1
    mean = daily_returns.mean()
    std = daily_returns.std()
    sharpe_ratio = np.sqrt(yearly_samples) * (np.mean(mean - risk_free_return) / std)

    return daily_returns, cumulative_return, mean, std, sharpe_ratio

def rebalance_portfolio(prices, allocations, initial_investment=1, already_normalized=False):
    if not already_normalized:
        prices = prices / prices.ix[0, :]

    alloced = prices * allocations
    daily_portfolio = alloced * initial_investment
    daily_portfolio_total = daily_portfolio.sum(axis=1)

    return daily_portfolio_total


def minimimize_sharpe_ratio(allocs, norm_prices):
    return get_sharpe_ratio(allocs, norm_prices) * -1

def get_sharpe_ratio(allocs, norm_prices):
    daily_allocated_portfolio_total = rebalance_portfolio(norm_prices, allocs, 1, True)
    daily_returns, cumulative_return, mean, std, sharpe_ratio = get_portfolio_statistics(daily_allocated_portfolio_total)

    return sharpe_ratio


def optimize_portfolio(sd=dt.datetime(2013,1,1), ed=dt.datetime(2014,1,1), \
    syms=['GOOG','QCOM','INTC','AMD'], gen_plot=False):

    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)                  # Collect data
    prices = prices_all[syms]

    norm_prices = prices / prices.ix[0, :]              # Normalize prices
    initial_allocations = [1.0 / len(syms)] * len(syms) # Init allocation: Fair distribution
    ranges = [(0.0,1.0)] * len(syms)                    # Limit opmitizer to only pick values for 0 to 1

    # Find optimal portfolio allocation
    allocations = spo.minimize(minimimize_sharpe_ratio, initial_allocations, args=(norm_prices,), options={"disp": False}, \
            method="SLSQP", bounds=ranges, constraints = ({ 'type': 'eq', 'fun': lambda inputs: inputs.sum() - 1 }))
    allocations = allocations['x']

    # With the chosen allocation distribution, compute portfolio statistics
    daily_allocated_portfolio_total = rebalance_portfolio(norm_prices, allocations, 1, True)
    daily_returns, cumulative_return, mean, std, sharpe_ratio = get_portfolio_statistics(daily_allocated_portfolio_total)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        prices_spy = prices_all["SPY"]
        normalized_spy = prices_spy / prices_spy[0]
        dftemp = pd.concat([daily_allocated_portfolio_total, normalized_spy], keys=['Optimized Portfolio', 'SPY'], axis=1)
        save_plot(dftemp, 'chart.png', ylabel='Normalized Price', title='Optimized Portfolio vs S&P500')
        pass

    return allocations, cumulative_return, mean, std, sharpe_ratio

def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    daily_allocated_portfolio_total = rebalance_portfolio(prices, allocs)
    daily_returns, cumulative_return, mean, std, sharpe_ratio = get_portfolio_statistics(daily_allocated_portfolio_total)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    return cumulative_return, mean, std, sharpe_ratio, daily_allocated_portfolio_total[-1]

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
