# -----------------------------------------------------------------------------------#
# USEFUL PSYCHOPY THINGS :) #
# -----------------------------------------------------------------------------------#

import numpy as np

import psychopy
import psychtoolbox as ptb
from psychtoolbox import PsychPortAudio

def wait_trigger(key=['5'], num=5):

    '''
    Wait for num triggers and record each trigger's time using PTB GetSecs()

    Args:
        key: list with all possible keys for scanner (default = 5; this is MPI 7T key)
        num: how many triggers to wait for

    Returns:
        trigger_init: time of firt trigger
        trigger_times: times of all triggers waited for
    '''

    response_kb = keyboard.Keyboard(backend='ptb')
    trigger_times = []

    for t in range(num):
        trigger_keys = trigger_kb.waitKeys(keyList=key, waitRelease=False)
        trigger_time = ptb.GetSecs()
        trigger_times[t] = trigger_time

    trigger_init = trigger_times[0]    

    return trigger_init, trigger_times

def open_audioport(fs, mode=1, latency=4, channels=1):

    '''
    Creates audio port

    Args:
        fs: sample rate
        mode: mode (1 = playback only)
        latency: latency mode (4 = strictest)
        channels: 1 = mono, 2 = stereo

    Returns:
        pahandle: audioport for further usage
    '''

    pahandle = PsychPortAudio('Open', [], mode, latency, fs, channels)

    return pahandle


def create_buffer_handle(sound):

    '''
    Creates buffer handle

    Args:
        sound: np array corresponding to sound

    Returns:
        buffer_handle: buffer handle for further usage
    '''

    sound = sound.astype(np.float32)
    buffer_handle = PsychPortAudio('CreateBuffer', [], sound)

    return buffer_handle


def play_from_buffer(pahandle, buffer_handles, ind): 

    '''
    Plays one sound from pre-created list of buffer handles

    Args:
        pahandle: pre-created pahandle
        buffer_handles: list of pre-created buffer handles
        ind: index (which buffer handle to play)

    Returns:
        onset: sound onset
    ''' 

    PsychPortAudio('UseSchedule', pahandle, 1)
    PsychPortAudio('AddToSchedule', pahandle, buffer_handles[ind])
    onset = PsychPortAudio('Start', pahandle, 1, 0, 1) 

    return onset     