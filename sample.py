import numpy as np
from raman_util.sample_spectra import n_peaks_spectra,polynomial_baseline
from raman_util import *


def sample_asPLS():
    from raman_util.arPLS import arPLS

    #generate simulated data
    x = np.arange(0,1000)
    y = n_peaks_spectra(x,n=3,seed=0) + polynomial_baseline(x,degree=3)

    #correct and show process
    correct = arPLS(y,show_process=True,guess_baseline_order=3)


if __name__ == "__main__":
    sample_asPLS()

    # import pandas as pd
    # import matplotlib.pyplot as plt
    # path = "/Users/FujisawaNoritaka/Documents/M1/codes/datas/MM_RamanData/20220620_MGUS/Results/1_Test/00hr/Data_set/1_Test_00hr_1.csv"
    # df = pd.read_csv(path,index_col=0)
    # cell0 = df.iloc[:750,0]
    
    # correct_arPLS   = arPLS.arPLS(cell0,show_process=True,guess_baseline_order=2)
    # #correct_pureASL = pureASL.pureASL(cell0,show_process=True)
    

