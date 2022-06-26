import numpy as np
import matplotlib.pyplot as plt
#import sample-1
#from raman_util.correct_baseline import *
#pureASL

#import sample-2
# from raman_util import *
# correct_baseline.arPLS()

#import sample-3
# import raman_util.load
# raman_util.load.load_ascs()


#XXX:Possible increase in baseline error as the maximum number of times increases.


if __name__ == "__main__":
    #generate simulated data
    from raman_util.sample_spectra import *
    from raman_util.correct_baseline import arPLS,_lambda_optimizer_to_arPLS
    x = np.arange(0,1000)
    true_data = n_peaks_spectra(x,n=3,seed=0)
    true_base = polynomial_baseline(x,degree=3)
    y = true_data + true_base

    #correct and show process
    max_loop = 10
    #baseline may 
    correct,base,info = arPLS(y,show_process=False,guess_baseline_order=3,full_output=True,loop_max=max_loop)
    l = info["lambda"]

    plt.plot(x,y,label="Target",alpha=0.3)
    plt.plot(x,true_data,label="TrueData",alpha=0.3)
    plt.plot(x,correct,label="MyMethod",alpha=0.3)

    if(False):#Comparison
        from pybaselines.whittaker import arpls as mod_arPLS
        base2,info = mod_arPLS(y,lam=l,max_iter=max_loop)
        plt.plot(x,y-base2,label="pybaselines",alpha=0.3)
    plt.legend()
    plt.show()

