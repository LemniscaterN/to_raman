import matplotlib.pyplot as plt
import numpy as np
import pybaselines
from pybaselines import utils
from sklearn.metrics import mean_squared_error
from pybaselines.whittaker import *
from raman_util.sample_spectra import *
from raman_util.correct_baseline import _lambda_optimizer_to_arPLS
import matplotlib

def optim_arPLS(x,order):
    lam = _lambda_optimizer_to_arPLS(len(x),order)
    return arpls(x,lam)

#Apply seviral methods, and calculate MSE.
if __name__ == "__main__":
    
    n = 6#Number of simulated data to be generated

    x = np.linspace(1, 1000, 1000)
    
    ys = []
    true_bases = []
    
    colors = list(matplotlib.colors.cnames.values())
    colors = colors[8:40]


    for i in range(n):
        true_bases.append(polynomial_baseline(x,degree=i+2,seed=i+5))
        ys.append(n_peaks_spectra(x,n=i+4,seed=0))

    
    funcs = [airpls,arpls,asls,aspls,derpsalsa,drpls,iarpls,iasls,psalsa]#optim_arPLS
    #orders=[2,3,3,4]# to optim_arPLS
    fig,axes= plt.subplots(2,n,figsize=(16,7))
    func_names = [x.__name__ for x in funcs]

    for i,y in enumerate(ys):
        signal = ys[i] + true_bases[i]
        mses = []
        
        axes[0][i].plot(signal,color="black",lw =1.5)
        axes[0][i].plot(true_bases[i],"--",color="black",lw =1.5)

        for j,func in enumerate(funcs):
            c = colors[j]
            if(func.__name__==optim_arPLS.__name__):
                bkg , _ = func(signal,order=orders[i])
            else:
                bkg , _ = func(signal,max_iter=60)
            axes[0][i].plot(bkg,'--',lw =1.5,color=c)
            mses.append(mean_squared_error(true_bases[i],bkg))
        axes[1][i].bar(func_names,mses,color=colors[0:len(funcs)])
        axes[1][i].set_yscale('log')
   
    func_names = [x.__name__ for x in funcs]
    label = ["Target","True_baseline"]
    label.extend(func_names)
    fig.legend(label)
    
    plt.subplots_adjust(left=0.04, right=0.97, bottom=0.05, top=0.95)
    fig.suptitle("Several Method & MSE(Mean Squared Error)")
    plt.show()