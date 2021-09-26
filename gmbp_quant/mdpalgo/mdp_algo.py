import numpy as np
from scipy.optimize import minimize
import json


def calc_diversification_ratio(w, v):
    # average weighted vol
    w_vol = np.dot(np.sqrt(np.diag(v)), w.T)
    # portfolio vol
    port_vol = np.sqrt(calculate_portfolio_var(w, v))
    diversification_ratio = w_vol / port_vol
    return diversification_ratio


def read_classification_file(file):
    with open(file) as j_file:
        raw_data = json.load(j_file)
    tickers = []
    classes = []
    weights = []
    for r in raw_data:
        tickers.append(r)
        classes.append(raw_data[r]["class"])
        weights.append(raw_data[r]["weight"])
    return tickers, weights, classes


#####################################################################
#               PORTFOLIO Optimization functions                    #
#####################################################################
# w: initial weight
# V: covariance matrix
# bnd: individual position limit
# long only: long only constraint

def calc_neg_diversification_ratio(w0, param):
    v = param[0]
    lmd = param[1]
    w = param[2]
    # average weighted vol
    w_vol = np.dot(np.sqrt(np.diag(v)), w0.T)
    # portfolio vol
    port_vol = np.sqrt(calculate_portfolio_var(w0, v))
    diversification_ratio = w_vol / port_vol
    # return negative for minimization problem (maximize = minimize -)

    punish = np.sum(np.power(np.array(w0) - np.array(w), 2))  # add punish to obj func

    return -diversification_ratio + lmd * punish


def calculate_portfolio_var(w, cov_mat):
    return np.dot(np.dot(w.T, cov_mat), w)


def max_div_portf(w0, v, bnd=None, long_only=True, lmd=0):
    param = [v, lmd, w0]
    cons = ({'type': 'eq', 'fun': total_weight_constraint},)
    if long_only:  # add in long only constraint
        cons = cons + ({'type': 'ineq', 'fun': long_only_constraint},)
    res = minimize(calc_neg_diversification_ratio, w0, bounds=bnd, args=param, method='SLSQP', constraints=cons)
    return res.x


def total_weight_constraint(w0):
    return np.sum(w0) - 1


def long_only_constraint(w0):
    return w0 - 0.01
