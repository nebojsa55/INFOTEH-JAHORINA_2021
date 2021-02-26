"""
@authors: Nebojsa Jovanovic (nebojsa.php@gmail.com)
          Nenad B. Popovic (nenad.pop92@gmail.com)
          Nadica Miljkovic (nadica.miljkovic@etf.rs)
          Faculty of Electrical Engineering, University of Belgrade
         
"""

if __name__ == '__main__':

    import os
    import numpy as np
    import scipy.signal
    import emd
    from utils import direct_autocorr
    from utils import FFT_max,PSD_welch
    from noise_modeling import *
    import matplotlib.pyplot as plt
    import tqdm
    
    # Parameters
    N = 2400 
    Nfft = 4096
    fs = 2 # Hz
    path = os.path.abspath(os.getcwd()) + '\Database'
    LF = 0.016 # Hz
    HF = 0.25 # Hz
    
    fosa = np.linspace(0,1,Nfft//2)
    
    # Load EGG signal
    data = np.loadtxt(path + '\ID1_fasting.txt').transpose()
    egg = data[1,:]
    
    # Preprocessing
    b,a = scipy.signal.butter(3,(LF,HF),'bandpass')
    egg = scipy.signal.filtfilt(b,a,egg)
    
    # Dominant frequency
    fftegg,df = FFT_max(egg,Nfft)
    
    noise_range = np.arange(-30,10,1)
    RD = []
    
    for snr in tqdm.tqdm(noise_range, total = len(noise_range)):
        # Adding noise 
        egg_noise = AWGN(egg,snr)
        
        # Performing EMD
        imfs = emd.sift.complete_ensemble_sift(egg_noise,nensembles = 16, max_imfs=8, nprocesses = 4)[0]
        Nimfs = len(imfs[0,:])
        # emd.plotting.plot_imfs(imfs, cmap=True, scale_y=True)
        
        # Statistical parameters from IMFs
        accPeaks = [direct_autocorr(imfs[:,i],0,2400,30,67)[1] for i in range(Nimfs)]
        dfs = [FFT_max(imfs[:,i],Nfft)[-1] for i in range(Nimfs)]
        peakMean = np.mean([x for x in accPeaks])
        peakStd = np.std([x for x in accPeaks])
                       
        #%% Prvi krug - FFT
        # sig = imfs[:,2] + imfs[:,3]
        # fftaa,aaaa = FFT_max(sig,Nfft)
        # plt.figure()
        # plt.plot(fosa,fftaa)
        
        sig1 = imfs[:,(np.array(dfs)>0.0167) & (np.array(dfs)<0.15)]
        Nsig = len(sig1[0,:])
        
        #%% Drugi krug - pikovi acc
        
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
        _,_,df3 = PSD_welch(egg_noise,fs,790)
        RD.append(np.abs(df2-df)*100/df)
        # plt.figure()
        # plt.plot(fosa,fft2)
    #%%
    
    plt.figure()
    plt.stem(noise_range,RD)
    plt.xlabel('SNR [dB]')
    plt.ylabel('Realtivna razlika [%]')