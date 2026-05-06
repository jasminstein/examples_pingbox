# -----------------------------------------------------------------------------------#
# Utils #
# -----------------------------------------------------------------------------------#

from scipy.io.wavfile import read, write

def read_wav(file):

    '''
    Reads .wav file

    Args:
        file: full path to file to be read

    Returns:
        fs: sample rate
        sound: array corresponding to sound    
    '''  

    fs, sound = read(file)

    return fs, sound


def write_wav(sound, fs, out_name, out_path): 

    '''
    Writes sound array to .wav file

    Args:
        sound: array corresponding to a sound
        fs: sample rate
        out_name: desired file name
        out_path: directory to which .wav file is saved
    '''     

    write(f"{out_path}/{out_name}.wav", fs, sound)