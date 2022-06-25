import numpy as np
#import sample-1
#from raman_util.correct_baseline import *
#pureASL

#import sample-2
# from raman_util import *
# correct_baseline.arPLS()

#import sample-3
# import raman_util.load
# raman_util.load.load_ascs()


if __name__ == "__main__":
    #generate simulated data
    from raman_util.sample_spectra import *
    from raman_util.correct_baseline import arPLS
    x = np.arange(0,1000)
    y = n_peaks_spectra(x,n=3,seed=0) + polynomial_baseline(x,degree=3)
    #correct and show process
    correct = arPLS(y,show_process=True,guess_baseline_order=3)
