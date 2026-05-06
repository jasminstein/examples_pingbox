# -----------------------------------------------------------------------------------#
# FUNCTIONS RELATING TO GENERATE SOUND STIMULI #
# -----------------------------------------------------------------------------------#

import numpy as np
from toolbox.loudness import compute_loudness_contour
from toolbox.operations import normalize

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
        sound = normalize(sound, reference = None)

    return sound 

def generate_f_from_greenwood(f_min, f_max, f_num):

    '''
    Generate frequencies based on Greenwood function (Cochlear spacing)

    Args:
        f_min: minimum frequency in Hz
        f_max: maximum frequency in Hz
        f_num: number of frequencies

    Returns:
        freqs: array containing frequencies in Hz
    '''
    
    aA = 165.4
    k = 0.88
    a = 2.1

    xmin = np.log10(f_min / aA + k) / a
    xmax = np.log10(f_max / aA + k) / a

    x_map = np.linspace(xmin, xmax, f_num)
    freqs = aA * (10**( a*x_map ) - k)

    return freqs  

def generate_pure_tone(f, fs, duration):

    '''
    Generate pure tone with specific frequency, sample rate, and duration

    Args:
        f: frequency in Hz
        fs: sample rate
        duration: duration in seconds

    Returns:
        sound: numpy array corresponding to pure tone
    '''

    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    sound = np.sin(2 * np.pi * f * t)

    return sound


def generate_white_noise(fs, duration, amplitude=1.0):

    '''
    Generate white noise with specific sample rate, duration, and amplitude

    Args:
        fs: sample rate
        duration: duration in seconds
        amplitude: amplitude (default = 1)

    Returns:
        sound: numpy array corresponding to white noise
    '''  

    sound = np.random.normal(0, 1, int(duration * fs)) 
    sound = sound*amplitude

    return sound


def generate_pure_tone_cloud(mean, std_dev, fs, duration, num, isi_frac=0.1, phon=65):


    ''' generate pure tone "clouds" from a mean and standard deviation

    Args:
        mean: mean of pure tone cloud
        std_dev: standard deviation of pure tone cloud
        fs: sample rate
        duration: full cloud duration in seconds
        num: numer of pure tones in cloud
        isi_frac: which fraction of full duration is supposed to be isi (sum of all ISIs)
        phon: phon level to normalize tones to

    Returns:
        sound_cloud: numpy array corresponding to pure tone cloud
    ''' 

    isi_duration = duration*isi_frac
    tone_duration = (duration - isi_duration)/num
    isi = isi_duration/(num - 1)

    sound = []

    freq = np.random.normal(loc=mean, scale=std_dev, size=num) # sample tones from normal distribution
    # TODO: find a better sampling method!
    
    for ind, f in enumerate(freq):

        t_sound = np.linspace(0, tone_duration, int(fs * tone_duration), endpoint=False)
        sound_n = np.sin(2 * np.pi * f * t_sound)

        sound_eq_iso, spl_required  = compute_loudness_contour(f, sound_n, phon) 
        sound.append(sound_eq_iso)

        #TODO: potentially add hanning windows to each sound
        
        if ind < (num-1):
            t_isi = np.zeros(int(isi*fs))
            sound.append(t_isi)


    sound_cloud = [x for sub in sound for x in sub]
    sound_cloud = np.array(sound, dtype=float)

    return sound_cloud            