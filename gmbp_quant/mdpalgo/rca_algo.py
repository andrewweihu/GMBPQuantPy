import numpy as np
from scipy.stats import pearsonr


def calc_portf_rtn(w0, rtn):
    return np.dot(w0.T, rtn)


def calc_portf_vol(w0, v):
    portf_var = np.dot(np.dot(w0.T, v), w0)
    port_vol = np.sqrt(portf_var)
    return port_vol


def calc_exp_return(std, spc, sp):
    return std * spc * sp


# return:
# 1. stock std
# 2. portf std
# 3. portf rtn
# 4. stock to portf correlation
# 5. stock risk contribution
def calc_risk_contribution(w0, rtn, inv):
    spc = []
    std = []
    src = []
    rtn_p = calc_portf_rtn(w0, rtn)  # get portf rtn with interval = inv
    std_p = np.std(rtn_p) * np.sqrt(250 / inv)  # get annualized portf std
    for i, r in enumerate(rtn):
        std_i = np.std(r) * np.sqrt(250 / inv)
        spc_i = pearsonr(r, rtn_p)[0]
        std.append(std_i)
        spc.append(spc_i)
        rc_i = w0[i] * std_i * spc_i / std_p
        src.append(rc_i)
    std = np.array(std)
    std_p = np.array(std_p)
    rtn_p = np.array(rtn_p)
    spc = np.array(spc)
    src = np.array(src)

    return std, std_p, rtn_p, spc, src, std_p