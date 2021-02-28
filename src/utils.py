"""
@authors: Nebojsa Jovanovic (nebojsa.php@gmail.com)
          Nenad B. Popovic (nenad.pop92@gmail.com)
          Nadica Miljkovic (nadica.miljkovic@etf.rs)
          University of Belgrade - School of Electrical Engineering
"""
import numpy as np
import scipy as sp
import scipy.signal
import scipy.fftpack
import pandas as pd
import math

def direct_autocorr(signal,start,samples,k_begin,k_end):
    
    """     
    Calculates the normalized autocorrelation of the signal in the range
    from "k_begin" to "k_end" in the signal "signal".  
    
    Inputs:
        signal -> signal for which normalized autocorrelation is calculated
        start -> index of the starting position of the signal for which 
                 autocorrelation is calculated
        samples -> the number of signal samples for which autocorrelation is 
                   calculated
        k_begin -> the initial lag of autocorrelation
        k_end -> the final lag of autocorrelation
        
    Outputs:
        acc_direct -> the normalized autocorrelation signal
        peak_direct -> value of the norm. acc. peak
        index_direct -> index of the norm. acc. peak
    
    """
    
    x = signal[start:start+samples]
    N = np.size(x)
    
    # Compute the normalized autocorrelation
    acc_direct = []
    
    for k in range(k_begin,k_end):
        numerator = np.sum(x[0:N-k-1]*x[k:N-1])
        denominator = np.sqrt(np.sum(x[k:N-1]*x[k:N-1]))*np.sqrt(np.sum(x[0:N-k-1]*x[0:N-k-1]))
        acc_direct.append(numerator/denominator)
        
    index,properties = sp.signal.find_peaks(acc_direct, height = (0.001,1))
    
    if index.any():
        index_direct = index[0] + k_begin
        peak_direct = properties['peak_heights']
        peak_direct = peak_direct[0]
    else:
        peak_direct = 0
        index_direct = 0
    
    return acc_direct,peak_direct,index_direct


def PSD_welch(signal,fs,window):
    
    """

    Calculates the Welch's spectrum given the scale which
    determines the lenght of the window like N/scale where 
    N is the signal length

    Inputs:
        signal -> signal for which Welch's spectrum is calculated
        fs -> sample frequency
        scale -> window_length = len(signal)/scale
        
    Outputs:
        PSD -> power spectral density
        f_PSD -> frequency axis of the calculated PSD
        f_dom -> the value of the dominant frequency in the given PSD   
    """
    
    noverlap = (240,window/2)[window <= 480]
    f_PSD,PSD = sp.signal.welch(signal,fs,nperseg = window,noverlap = noverlap)

    f_dom = np.argmax(PSD[0:int(np.round(np.size(PSD)*0.08))])
    f_dom = f_PSD[f_dom]
    
    return PSD,f_PSD,f_dom


def FFT_max(signal,Nfft):
    
    """
    
    Find the maximum in FFT of the signal
    
    Inputs:
        signal -> signal for which FFT is calculated
        Nfft -> the number of points at which the FFT is calculated
        
    Outputs:
        fftsig -> Fast Fourier Transform of the given signal
        f_dom -> the value of the dominant frequency in the given FFT
    """
    
    fftsig = sp.fftpack.fft(signal,Nfft)
    fftsig = fftsig[0:Nfft//2]
    fftsig = np.abs(fftsig)
    
    border_frequency = 0.167
    index = int(np.round(Nfft/2*border_frequency))
    f_dom = np.argmax(fftsig[0:index])
    f_dom = f_dom/(Nfft/2)

    return fftsig,f_dom
    

  

    
