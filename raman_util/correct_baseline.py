"""
    To correct baseline.
    * arPLS
    * purePLS
    * rolling_ball
"""

from scipy import sparse
from scipy.sparse import linalg
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix
from scipy.sparse import spdiags
import scipy.sparse.linalg as spla
import pandas as pd


#Paper about arPLS
#https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b

#Original:StackOverFlow
#https://stackoverflow.com/questions/29156532/python-baseline-correction-library?answertab=createdasc#tab-top
def arPLS(  
        Data                  :list,
        lam                   :int  =1e4, 
        ratio                 :float=1e-6, 
        loop_max              :int  =10, 
        show_process          :bool =False,
        full_output           :bool =False,
        guess_baseline_order  :int  =None,
        
    ):
    """
        arPLS(2014)

        Parameters
        ----------
        Data            
        lam                   : Smoothing and fitting balancing parameters.
        ratio,loop_max        : Exit condition. 
        guess_baseline_order : To use optimized lambda. See your data , and gusess baseline order.

        Return
        ----------
        corrected,(estimate_baseline,info)
    """
    L = len(Data)
    if(guess_baseline_order is not None):
        lam = _lambda_optimizer_to_arPLS(L,guess_baseline_order)

    diag = np.ones(L - 2)
    D = sparse.spdiags([diag, -2*diag, diag], [0, -1, -2], L, L - 2)
    H = lam * D.dot(D.T)  # The transposes are flipped w.r.t the Algorithm on pg. 252
    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)
    criteria = 1
    count = 0
    plt.plot(Data,color="black",label="Target")

    while criteria > ratio:
        estimate_baseline = linalg.spsolve(W + H, W * Data)
        d = Data - estimate_baseline
        dn = d[d < 0]
        m = np.mean(dn)
        s = np.std(dn)

        #2 * (d - (2*s - m))/s  > 1000,np.exp(tes)=inf
        with np.errstate(all='ignore'):   
            ex = np.exp(2 * (d - (2*s - m))/s) 
        w_new = 1 / (1 + ex)
    
        criteria = norm(w_new - w) / norm(w)
        w = w_new
        W.setdiag(w)  # Do not create a new matrix, just update diagonal values
        count += 1
        plt.plot(estimate_baseline, "black", linewidth=1, linestyle="dashed",alpha=0.3)

        if count > loop_max:
            print('Maximum number of iterations exceeded.')
            break
    
    if show_process:
        plt.title(f"arPLS $\lambda$={lam:.2f}")
        plt.plot(estimate_baseline,"black", linewidth=1, linestyle="dashed",label="Estimated Baseline")
        plt.plot(Data-estimate_baseline,color="blue",label="Corrected")
        plt.legend()
        plt.show()
    plt.clf()
    plt.close()

    if full_output:
        info = {'num_iter': count, 'stop_criteria': criteria,'lambda':lam}
        return  d,estimate_baseline,info
    else:
        return d

#Asymetrically reweighted penalized least squares[2019]
#https://www.koreascience.or.kr/article/JAKO201913458198163.pdf
def _lambda_optimizer_to_arPLS(input_length,baseline_order_from_shape):
    N = input_length
    t = baseline_order_from_shape
    lam = 10**(np.log2(N)-0.5*t-3.5)
    return lam

#Maybe this code is original.
#https://stackoverflow.com/questions/29156532/python-baseline-correction-library
def pureASL(
        Data            :list,
        lam             :int   =10**3.5,
        p               :float =0.00005,
        repeat_max      :int   =10,
        show_process    :bool  =False
    ):
    """
        Asymmetric Least Squares Smoothing(2005)
        In practice, λ and p need to be optimized.
        λ : 1e3-1e5 ?
        p : 0.001-0.1
    """ 
    L = len(Data)
    D = csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    plt.plot(Data,color="black",label="Targets")

    y = 0
    corrected = pd.DataFrame(index=range(len(Data)))
    for i in range(repeat_max):
        W = spdiags(w, 0, L, L)
        Y = W + lam * D.dot(D.transpose())
        y = spla.spsolve(Y, w*Data)
        w = p * (Data > y) + (1-p) * (Data < y)
        corrected.loc[:, i+1] = Data - y
        plt.plot(y, "black", linewidth=1, linestyle="dashed",alpha=0.3)

    if show_process:
        plt.title(f"pureASL λ={lam:.2f},p={p}")
        plt.plot(y, "black", linewidth=1, linestyle="dashed",label="Estimated Baseline")
        plt.plot(corrected.loc[:, repeat_max],color="blue",label="Corrected")
        plt.legend()
        plt.show()
    plt.clf()
    plt.close()
    return corrected.loc[:, repeat_max]


def rolling_ball(
        Data        :list,
        radius      :int,
        show_process:bool=False
    ):
    """
        Rolling_ball(kimage.restoration)
        In practice, radius need to be optimized.
    """ 
    from skimage.restoration import rolling_ball as rb
    estimated_background = rb(Data, radius=radius)    
    if show_process:
        plt.plot(Data,color="black",label="Targets")
        plt.plot(estimated_background, "black", linewidth=1, linestyle="dashed",label="Estimated Baseline")
        plt.plot(Data-estimated_background,color="blue",label="Corrected")
        plt.title(f"Rolling_ball radius={radius}")
        plt.legend()
        plt.show()
        plt.clf()
        plt.close()
    return Data - estimated_background

if __name__ == "__main__":
    import sample_spectra
    from sample_spectra import n_peaks_spectra,polynomial_baseline
    x = np.arange(1, 1001)
    y = sample_spectra.n_peaks_spectra(x,n=3) + sample_spectra.polynomial_baseline(x,degree=4,seed=1)
    corrected = arPLS(y,show_process=True,guess_baseline_order=3)
    corrected = arPLS(y,show_process=True,lam=1e4) 
    corrected = pureASL(y,show_process=True)
    for radius in np.arange(1,30,6):
        corrected = rolling_ball(y,radius,show_process=True)
