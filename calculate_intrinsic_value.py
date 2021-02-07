'''
Calculates the intrinsic value of a company based on Warren Buffet method.
Requires free cash flow, discount rate, and future growth estimates as input.
'''

import numpy as np


def calculate_fcf(byfcf, gr, n):
    """
    Calculates free cash flow n years into the future.
    :param byfcf: Base year free cash flow
    :param gr: Estimated growth rate
    :param n: num years into the future (we're calculating for this year)
    :return: Free cash flow n years into the future
    """
    return byfcf * (pow(1 + gr, n))


def calculate_df(dr, n):
    """
    Calculates discount rate n years into the future.
    :param dr: discount rate
    :param n: num years into the future
    :return: Discount rate for the year n
    """
    return pow(1 + dr, n)

if __name__ == '__main__':
    print(calculate_fcf(20931.0, 0.15, 10))
    print(calculate_df(0.2, 10))

