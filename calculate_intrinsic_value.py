"""
Calculates the intrinsic value of a company based on Warren Buffet method.
Requires free cash flow, discount rate, and future growth estimates as input.
"""


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


def calculate_dfcf(byfcf, gr, n, dr):
    """
    Calculates discounted free cash flow n years into the future
    :param byfcf: Base year free cash flow
    :param gr: Estimated growth rate
    :param n: num years into the future (we're calculating for this year)
    :param dr: discount rate
    :return: free cash flow n years into the future
    """
    return calculate_fcf(byfcf, gr, n) / calculate_df(dr, n)


def calculate_dpfcf(byfcf, gr, dr, lgr):
    """
    Returns discounted perpetuity free cash flow (11 years into the future)
    :param byfcf: Base year free cash flow
    :param gr: Estimated growth rate
    :param n: num years into the future (we're calculating for this year)
    :param dr: discount rate
    :param lgr: long-term growth rate
    :return: discounted perpetuity free cash flow
    """
    return (((byfcf * pow(1 + gr, 11)) * (1 + lgr)) / (dr - lgr)) * (1 / pow(1 + dr, 11))


def calculate_iv(byfcf, gr, dr, lgr):
    """
    Returns intrinsic value for company
    :param byfcf: Base year free cash flow
    :param gr: Estimated growth rate
    :param dr: discount rate
    :param lgr: long-term growth rate
    :return: intrinsic value for company (whole company, not per share)
    """
    iv = 0
    for i in range(10):
        n = i + 1
        iv += calculate_dfcf(byfcf, gr, n, dr)
    iv += calculate_dpfcf(byfcf, gr, dr, lgr)
    return iv


if __name__ == '__main__':
    ticker = 'MKL'
    current_fcf = 1.209
    growth_rate = 0.15
    discount_rate = 0.2
    long_term_growth = 0.1
    shares_outstanding = 0.014

    print(f'Intrinsic value per share ({ticker}): {round(calculate_iv(current_fcf, growth_rate, discount_rate, long_term_growth) / shares_outstanding, 2)}$')
