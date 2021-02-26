# Open-access EGG Database

Electrogastrograms ([EGG](https://en.wikipedia.org/wiki/Electrogastrogram)) used in this paper are freely available at the Zenodo repository [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3878435.svg)](https://doi.org/10.5281/zenodo.3878435)

## Description

The database consists of EGGs recorded in 20 healthy volunteers on three channels (**CH1**, **CH2**, **CH3**) and two states (**fasting** and **postprandial**). Sample rate is set at *fs* = 2 Hz. Gain of the amplifier is 1000. All signals were filtered with 3rd order band-pass Butterworth filter with cut-off frequencies of 0.03 Hz and 0.25 Hz as described in [Popović et al. 2019](https://www.degruyter.com/document/doi/10.1515/bmt-2017-0218/html). 

### Naming convention

*subject'sID _ type of recording* (**fasting / postprandial**).txt

*An example*: 
> ID9_fasting.txt (**subject ID9 in fasting state**)

Every .txt file is presented in 2400 x 3 format (**number_of_samples** x **number_of_channels**)


---------------------------------------------------------------------------------------------------------------------------------------------------------

If you find these signals useful for your own research, please cite relevant papers and dataset as:

1. Popović, N.B., Miljković, N. and Popović, M.B., 2019. Simple gastric motility assessment method with a single-channel electrogastrogram. *Biomedical Engineering/Biomedizinische Technik*, *64*(2), pp.177-185, doi: [10.1515/bmt-2017-0218](https://doi.org/10.1515/bmt-2017-0218).
2. Popović, N.B., Miljković, N. and Popović, M.B., 2020. Three-channel surface electrogastrogram (EGG) dataset recorded during fasting and post-prandial states in 20 healthy individuals [Data set]. *Zenodo*, doi: [10.5281/zenodo.3730617](https://doi.org/10.5281/zenodo.3730617).
