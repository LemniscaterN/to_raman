import numpy as np
from raman_util import sample_spectra
from raman_util.pureASL import pureASL
from raman_util.sample_spectra import n_peaks_spectra,polynomial_baseline
from raman_util.arPLS import arPLS

#If you import module like this,
#from raman_util import *

#You can use like those.(Caution:Both of module and function are same name.)
#pureASL.pureASL()
#sample_spectra.n_peaks_spectra()
#pureASL.pureASL()

if __name__ == "__main__":
    

    #generate simulated data
    x = np.arange(0,1000)
    y = n_peaks_spectra(x,n=3,seed=0) + polynomial_baseline(x,degree=3)
    #correct and show process
    correct = arPLS(y,show_process=True,guess_baseline_order=3)
