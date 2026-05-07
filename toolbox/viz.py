# -----------------------------------------------------------------------------------#
# VISULIZATIONS #
# -----------------------------------------------------------------------------------#

import matplotlib.pyplot as pyplot

def plot_signal(sound, fs):

    '''
    Plot sound 

    Args:
        sound: array for sound
        fs: sample rate
    '''

    t = np.arange(len(sound)) / fs

    plt.figure(figsize=(10, 4))
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()


def plot_spectrum(sound, fs):

    '''
    Plot frequency spectrum 

    Args:
        sound: array for sound
        fs: sample rate
    '''

    n = len(sound)
    freq = np.fft.rfftfreq(n, d=1/fs)  
    fft_data = np.fft.rfft(sound)
    magnitude = np.abs(fft_data) 

    plt.plot(freq, magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (non-normalized)")
    plt.show()
   