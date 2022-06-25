
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def n_peaks_spectra(
        x,
        n=3,
        seed=0,
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


def polynomial_baseline(x,degree=3):
    """
        Generate degree baseline
    """
    y = 100*np.cos(x/(len(x)/(3*np.pi)))
    # plt.plot(y)
    # plt.show()
    coef=np.polynomial.Polynomial.fit(x, y, deg=degree)
    return coef(x)
    

if __name__ == "__main__":
    x = np.arange(1, 3001)
    for i in range(3):
        sim = n_peaks_spectra(x,n=3,seed=i)
        base = polynomial_baseline(x)
        y = sim + base
        plt.plot(y,label="Created")
        plt.plot(base,label="baseline")
        plt.plot(sim,label="sim")
        plt.legend()
        plt.show()