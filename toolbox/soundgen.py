# -----------------------------------------------------------------------------------#
# FUNCTIONS RELATING TO GENERATE SOUND STIMULI #
# -----------------------------------------------------------------------------------#

import numpy as np

def geometric_decay(num, harmonic_factor):

    '''
    Function to create more generalizable implementation of harmonics

    Args:
        num: number of harmonics
        harmonic_factor: harmonic decay factor

    Returns:
        list of harmonics and corresponding amplitudes
    '''
        
    return [
        (k, harmonic_factor ** (k - 1))
        for k in range(1, num)
    ]

def generate_hct(f0, fs, duration, num, harmonics_type='1/n', harmonic_factor=0.6, normalize=False):

    '''
    Function to create harmonic complex tones

    Args:
        f0: fundamental frequency
        fs: sample rate
        duration: sound duration in seconds
        harmonics_type: string (from dict below; default = 1/n)
        harmonic_factor: harmonic factor in case geometric_decay is used (default = 0.6)
        normalize: normalize final sound by its max. ampitude (default = False)

    Returns:
        list of harmonics and corresponding amplitudes
    '''

    harmonics_dict =  {
        "1/n": [(n, 1/n) for n in range(1, num)], 
        "1/n^2": [(n, 1/(n**2)) for n in range(1, num)],
        "e^(-0.5(n-1))": [(n, np.exp(-0.5*(n - 1))) for n in range(1, num)],
        "odd 1/n": [(n, 1/n) for n in range(1, num, 2)],
        "geometric_decay": geometric_decay(num, harmonic_factor)
        }

    harmonics = harmonics_dict[harmonics_type]
    
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    sound = np.zeros_like(t)

    for multiple, amplitude in harmonics:
        sound += amplitude * np.sin(2 * np.pi * f0 * multiple * t)

    if normalize:
        sound /= np.max(np.abs(sound))

    return sound    