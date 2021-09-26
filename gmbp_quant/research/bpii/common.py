import pandas as pd
import numpy as np

THRESHOLD_LmA = 2.4
THRESHOLD_L = 5


def get_buy_type(bpii_large, bpii_average):
    buy_type = 0
    if bpii_large - bpii_average > THRESHOLD_LmA:
        buy_type += 1
    #
    if bpii_large > THRESHOLD_L:
        buy_type += 1
    #
    return buy_type
#


def get_divergence_indicator(pha=None, bpii_large=None, bpii_average=None):
    if pha is None:
        if bpii_large is None or bpii_average is None:
            raise Exception(f"Please provide either 'pha' or ('bpii_large','bpii_average') !")
        #
        pha = (bpii_large - bpii_average) / abs(bpii_average)
    #

    if pha == -np.inf:
        pha = -1e5
    elif pha == np.inf:
        pha = 1e5
    #

    di = pd.cut([pha],
                bins=[-np.inf, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, np.inf],
                labels=[-4, -3, -2, -1, 1, 2, 3, 4])
    return int(di[0]), pha
#
