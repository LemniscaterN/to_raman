
import itertools
import matplotlib.pyplot as plt

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import spdiags
import scipy.sparse.linalg as spla
import pandas as pd

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


if __name__ == "__main__":
    from sample_spectra import n_peaks_spectra,polynomial_baseline
    x = np.arange(1, 1001)
    y = n_peaks_spectra(x,seed=1) + polynomial_baseline(x)
    corrected = pureASL(y,show_process=True)
