# -----------------------------------------------------------------------------------#
# FUNCTIONS RELATING TO PITCH PERCEPTION #
# -----------------------------------------------------------------------------------#

import numpy as np

def hz_to_erb_rate(f):

    '''
    Convert Hz to ERB-rate according to Glassberg & Moore (1990)
    ATTENTION: e.g. the auditory modeling toolbox uses values 21.366 and 4.368

    Args:
        f: frequency in Hz

    Returns:
        erb_rate: corresponding ERB-rate
    '''
    
    erb_rate = 21.4 * np.log10(4.37 * f / 1000 + 1)

    return erb_rate

def erb_rate_to_hz(erb_rate):

    '''
    Convert ERB-rate to Hz according to Glassberg & Moore (1990)
    ATTENTION: e.g. the auditory modeling toolbox uses values 21.366 and 4.368

    Args:
        erb_rate: ERB-rate

    Returns:
        f: corresponding frequency in Hz
    '''

    f = (10 ** (erb_rate / 21.4) - 1) * (1000 / 4.37)  

    return f  