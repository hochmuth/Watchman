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
        # print(f'Calculating for year {n}')
        iv += calculate_dfcf(byfcf, gr, n, dr)
        # print(f'IV = {iv}')
    iv += calculate_dpfcf(byfcf, gr, dr, lgr)
    return iv


if __name__ == '__main__':
    print(f'Free cash flow in ten years: {calculate_fcf(20931.0, 0.15, 10)}')
    print(f'Discount factor of ten years: {calculate_df(0.2, 10)}')
    print(f'Discounted free cash flow in ten years: {calculate_dfcf(20931.0, 0.15, 10, 0.2)}')
    print(f'Discounted perpetuity free cash flow: {calculate_dpfcf(20931.0, 0.15, 0.2, 0.1)}')
    print(f'Intrinsic value: {calculate_iv(20.931, 0.15, 0.2, 0.1)}B')

    print(f'Intrisinc value per share: {calculate_iv(20.931, 0.15, 0.2, 0.1) / 4.232}$')
