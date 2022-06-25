

from scipy import sparse
from scipy.sparse import linalg
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

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
        corrected
    """
    L = len(Data)
    if(guess_baseline_order is not None):
        lam = _lambda_optimizer(L,guess_baseline_order)

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
        info = {'num_iter': count, 'stop_criteria': criteria,'lambda:':lam}
        return  d,estimate_baseline,info
    else:
        return d

#Asymetrically reweighted penalized least squares[2019]
#https://www.koreascience.or.kr/article/JAKO201913458198163.pdf
def _lambda_optimizer(input_length,baseline_order_from_shape):
    N = input_length
    t = baseline_order_from_shape
    lam = 10**(np.log2(N)-0.5*t-3.5)
    return lam

if __name__ == "__main__":
    import sample_spectra
    x = np.arange(1, 1001)
    y = sample_spectra.n_peaks_spectra(x,n=3) + sample_spectra.polynomial_baseline(x,degree=3)
    corrected = arPLS(y,show_process=True,guess_baseline_order=3)
    #corrected = arPLS(y,show_process=True,lam=1e4)