"""
    To generate simulation spectra.
    * n_peaks_spectra
    * polynomial_baseline
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


def n_peaks_spectra(
        x:list,
        n:int=3,
        seed:int=0,
    ):
    """
        Generate n-peaks data
    """
    L = len(x)
    np.random.seed(seed)
    coeff = np.random.randint(int(L/15) ,int(L/2)    ,n)
    mean  = np.random.randint(int(L/10) ,int(9*L/10) ,n)
    stdv  = np.random.randint(int(L/50) ,int(L/40)    ,n)
    terms = []
    for ind in range(n):
        term = coeff[ind] * np.exp(-((x - mean[ind]) / stdv[ind])**2)
        terms.append(term)
    spectra = sum(terms)
    return spectra


def polynomial_baseline(
        x:list,
        degree:int=3,
        seed:int=0,
    ):
    """
        Generate degree baseline
    """
    np.random.seed(seed)
    L = len(x)
    y=np.zeros(L)
    #generate random wave , and polyminal degree.
    for i in range(10):
        xi = x + np.random.randint(0,L/2)
        coef = np.random.random_sample()
        period = 2*np.pi*np.random.randint(1,8)#wave cnt in xrange
        y1 = 1000*coef*np.sin(period/(len(x))*(xi))
        y+=y1
    coef=np.polynomial.Polynomial.fit(x,y, deg=degree)
    # plt.plot(coef(x),label=f"coef:{degree}")
    # plt.legend()
    # plt.show()
    return coef(x)
    

if __name__ == "__main__":
    x = np.arange(1,3000)
    for i in range(3):
        n=i+1
        deg=i+2
        sim = n_peaks_spectra(x,n=n,seed=i)
        base = polynomial_baseline(x,degree=deg,seed=i)
        y = sim + base
        plt.plot(y,label=f"{n}-peaks")
        plt.plot(base,label=f"{deg}-degree-baseline")
        plt.plot(sim,label="Synthetic")
        plt.legend()
        plt.show()