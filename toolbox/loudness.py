# -----------------------------------------------------------------------------------#
# FUNCTIONS TO ADJUST PERCEIVED STIMULUS LOUDNESS #
# -----------------------------------------------------------------------------------#

from pydsm.iso226 import iso226_spl_itpl
import numpy as np

def compute_loudness_gain(f, sound, phon=65):
    
    '''
    Apply equal loudness contours as described by ISO226 (attention: only valid for pure tones)

    Args:
        f: pure tone frequency
        sound: array corresponding to pure tone
        phon: desired loudness level in phons (default = 65)

    Returns:
        sound_eq_iso: modified sound set to db SPL level corresponding to indicated phons
        spl_required: db SPL level to which sound was set to achieve equal loudness
    '''

    itpl = iso226_spl_itpl(phon)
    spl_required = itpl(f)
    sound_eq_iso = set_dbspl(sound, spl_required)
    
    return sound_eq_iso, spl_required 

def set_db_spl(sound, spl):

    '''
    Set db SPL level for a given sound (from: https://github.com/mrkrd/thorns/blob/master/thorns/waves.py) 

    Args:
        sound: array corresponding to a 
        spl: desired sound pressure level in db

    Returns:
        sound_out: sound rescaled to required db SPL   
    '''

    p0 = 20e-6
    rms = np.sqrt(np.sum(sound**2) / sound.size)

    sound_out = sound * 10**(dbspl / 20.0) * p0 / rms

    return sound_out    
