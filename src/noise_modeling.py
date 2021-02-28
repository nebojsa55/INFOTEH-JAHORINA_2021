"""
@authors: Nebojsa Jovanovic (nebojsa.php@gmail.com)
          Nenad B. Popovic (nenad.pop92@gmail.com)
          Nadica Miljkovic (nadica.miljkovic@etf.rs)
          University of Belgrade - School of Electrical Engineering
"""

import numpy as np
import emd

def AWGN(signal,snr):
    """
    Adds white Gaussian noise to the desired signal.
    
    Parameters:
        singal -> a signal to which the noise is added
        snr -> Signal to Noise ratio in dB
    Outputs:
        Signal with added noise
    """
    
    # Calculate signal power and convert to dB 
    sig_avg_watts = np.mean(signal ** 2)
    sig_avg_db = 10 * np.log10(sig_avg_watts)
    
    noise_avg_db = sig_avg_db - snr
    noise_avg_watts = 10 ** (noise_avg_db / 10)
    
    # Generate samples of white noise
    noise = np.random.normal(0, np.sqrt(noise_avg_watts), len(signal))
    
    # Return the noised signal
    
    return signal + noise   

def AWGN_dynamic(signal,snr):
    """
    Adds dynamic white Gaussian noise that increases amplitude over time to the
    desired signal.
    
    Parameters:
        singal -> a signal to which the noise is added
        snr -> Signal to Noise ratio in dB
    Outputs:
        Signal with added noise
    """
    
    # Calculate signal power and convert to dB 
    sig_avg_watts = np.mean(signal ** 2)
    sig_avg_db = 10 * np.log10(sig_avg_watts)
    
    noise_avg_db = sig_avg_db - snr
    noise_avg_watts = 10 ** (noise_avg_db / 10)
    
    # Generate samples of white noise
    am = np.linspace(0, 1, len(signal))**2 + .1
    noise = am * np.random.normal(0, np.sqrt(noise_avg_watts), len(signal))
    
    # Return the noised signal
    
    return signal + noise    
    
    
