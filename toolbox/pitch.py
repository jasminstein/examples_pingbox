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

def map_arbitrary_scale_erb(x_in, x_min=-1, x_max=1, f_min=500, f_max=1300):

    '''
    Maps an experimental frequency range (f_min to f_max) to ERB, linearly interpolates for a given range, and maps to Hz
    --> aim: equal steps in x_in result in PERCEPTUALLY equal steps on Hz scale

    Args:
        x_in: arbitrary value between x_min and x_max
        x_min: minimum value on arbitrary scale (default = -1)
        x_max: maximum value on arbitrary scale (default = 1)
        f_min: minimum f used in experiment in Hz (default = 500 Hz; based on Jasmin's experimental setup)
        f_max: maximum f used in experiment in Hz (default = 1300 Hz; based on Jasmin's experimental setup)

    Returns:
        f: frequency corresponding to x_in in Hz
    '''
    
    
    if np.any(x_in < x_min) or np.any(x_in > x_max):
        raise ValueError(
            f"x_input must be within [{x_min}, {x_max}], "
            f"but got {x_input}"
        )

    e_min = hz_to_erb_rate(f_min)
    e_max = hz_to_erb_rate(f_max)

    e = e_min + (e_max - e_min) * (x_in - (x_min)) / (x_max - (x_min))

    f = (10 ** (e / 21.4) - 1) * (1000 / 4.37)       

    return f   