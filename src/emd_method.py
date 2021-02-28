"""
@authors: Nebojsa Jovanovic (nebojsa.php@gmail.com)
          Nenad B. Popovic (nenad.pop92@gmail.com)
          Nadica Miljkovic (nadica.miljkovic@etf.rs)
          University of Belgrade - School of Electrical Engineering         
"""

import os
import numpy as np
import scipy.signal
import emd
from utils import direct_autocorr
from utils import FFT_max
from noise_modeling import *
import matplotlib.pyplot as plt
import tqdm
import time

if __name__ == '__main__':

    # Parameters
    N = 2400 
    Nfft = 4096
    fs = 2 # Hz
    path = os.path.abspath(os.path.join(os.getcwd(),os.pardir)) + '\Database'
    LF = 0.016 # Hz
    HF = 0.25 # Hz
    pmax_ref = 0.5
        
    # Load EGG signal
    data = np.loadtxt(path + '\ID1_fasting.txt').transpose()
    egg = data[1,:]
    
    # Preprocessing
    b,a = scipy.signal.butter(3,(LF,HF),'bandpass')
    egg = scipy.signal.filtfilt(b,a,egg)
    
    # Dominant frequency
    fftegg,df = FFT_max(egg,Nfft)
    
    noise_range = np.arange(-50,20,5)
    RD = []
    cert = []
    TIMES = []

    for snr in tqdm.tqdm(noise_range, total = len(noise_range)):
        # Adding noise 
        np.random.seed(0)
        egg_noise = AWGN(egg,snr)
        # egg_noise = AWGN_dynamic(egg,snr)
        
        # Performing EMD
        start = time.process_time()
        imfs = emd.sift.sift(egg_noise)
        # imfs = emd.sift.ensemble_sift(egg_noise,nensembles = 64,max_imfs = 5)
        TIMES.append(time.process_time()-start)
        Nimfs = len(imfs[0,:])
        # emd.plotting.plot_imfs(imfs, cmap=True, scale_y=True)
        
        # Statistical parameters from IMFs
        accPeaks = [direct_autocorr(imfs[:,i],0,2400,30,67)[1] for i in range(Nimfs)]
        dfs = [FFT_max(imfs[:,i],Nfft)[-1] for i in range(Nimfs)]
                       
        #%% First part - elimination based on FFT
        
        sig1 = imfs[:,(np.array(dfs)>0.0167) & (np.array(dfs)<0.167)]
        Nsig = len(sig1[0,:])
        
        #%% Second part - autocorrelation
    
        pmax = 0
        for numOfMixed in range(Nsig):
            for i in range(Nsig-numOfMixed):
                temp = sig1[:,i]
                for j in range(numOfMixed):
                    temp = temp + sig1[:,i+j+1]
                _,peak,_ = direct_autocorr(temp,0,2400,30,67)
                if peak>pmax:
                    pmax = peak
                    sig2 = temp
        #%%
        fft2,df2 = FFT_max(sig2,Nfft)
        cc = pmax/pmax_ref*100
        
        if cc>100: cc = 100
        
        RD.append(np.abs(df2-df)*100/df)
        cert.append(cc)
    #%%
    
    plt.figure()
    plt.stem(noise_range,RD)
    plt.xlabel('SNR [dB]')
    plt.ylabel('RD[%]')
    plt.figure()
    plt.stem(noise_range,cert)
    plt.xlabel('SNR [dB]')
    plt.ylabel('Certainty [%]')
    
