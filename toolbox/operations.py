# -----------------------------------------------------------------------------------#
# FUNCTIONS TO PERFORM SIMPLE OPERATIONS ON SOUND STIMULI #
# -----------------------------------------------------------------------------------#

import numpy as np
import scipy.signal
from scipy.signal import firwin, filtfilt

def resample(sound, fs, target_fs):

    '''
    Resample sound from given sample rate to target sample rate

    Args:
        sound: array corresponding to sound
        fs: current sample rate
        target_fs: desired sample rate

    Returns:
        resampled_sound: sound array at desired sample rate
    '''

    num_samples = int(len(sound)*target_fs/fs)
    resampled_sound = scipy.signal.resample(sound, num_samples, axis = 0)

    return resampled_sound


def apply_hanning(sound, fs, ramp_time):

    '''
    Apply hanning window to given sound

    Args:
        sound: array corresponding to sound
        fs: current sample rate
        ramp_time: ramp duration in seconds

    Returns:
        sound_out: sound incl. applied hanning window
    '''

    ramp_samples = int(fs * ramp_time)
    full_window = np.hanning(2 * ramp_samples)
    ramp_in = full_window[:ramp_samples]
    ramp_out = full_window[ramp_samples:]

    envelope = np.ones_like(sound)
    envelope[:ramp_samples] *= ramp_in
    envelope[-ramp_samples:] *= ramp_out

    sound_out = sound * envelope

    return sound_out


def bandpass_filter(sound, fs, lowcut, highcut, numtaps=2001): 

    '''
    Apply bandpass filter (using FIR filter) to given sound

    Args:
        sound: array corresponding to sound
        fs: current sample rate
        lowcut: lower limit of filter
        highcut: upper limit of filter
        numtaps: Length of the filter (number of coefficients, i.e., the filter order + 1). numtaps must be odd if a passband includes the Nyquist frequency.

    Returns:
        sound_out: bandpass-filtered sound array
    '''

    fir_coeffs = firwin(numtaps,
                        [lowcut, highcut],
                        pass_zero=False,
                        fs=fs)

    sound_out = filtfilt(fir_coeffs, [1.0], sound)  

    return sound_out 

def normalize(sound, reference=None):

    '''
    Normalizes sound to amplitude 1 or by a chosed reference value (e.g. an empirically defined overall maximum value)

    Args:
        sound: array corresponding to sound
        reference: if desired different reference value to normalize by

    Returns:
        sound_out: normalized sound
    '''

    sound = np.asarray(sound, dtype=float)

    if reference is None:
        sound_out = sound / np.max(np.abs(sound)) 
    else:
        sound_out = sound / reference

    return sound_out         