# stats101a.py
# from: https://realpython.com/python-statistics/
#
import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd


if __name__ == "__main__":

    x = [8.0, 1, 2.5, 4, 28.0]
    x_with_nan = [8.0, 1, 2.5, math.nan, 4, 28.0]
    
    """
    print('x: ', x)
    print('x_with_nan: ', x_with_nan)
    print('---')
    """
    """
    print(math.isnan(np.nan), np.isnan(math.nan))
    print(math.isnan(x_with_nan[3]), np.isnan(x_with_nan[3]))
    """
    
    y, y_with_nan = np.array(x), np.array(x_with_nan)
    z, z_with_nan = pd.Series(x), pd.Series(x_with_nan)
    """
    print('---')
    print('y: ', y)
    print('y_with_nan: ', y_with_nan)
    print('---')
    print('z: \n', z)
    print('z_with_nan: \n', z_with_nan)
    """
    """
    print('---')
    mean_ = sum(x) / len(x)
    print('pure python mean: ', mean_)
    
    print('---')
    mean_ = statistics.mean(x)
    print('built-in python: ', mean_)

    mean_ = statistics.fmean(x)
    print('built-in python f: ', mean_)

    mean_ = statistics.mean(x_with_nan)
    print('built-in python w/nan: ', mean_)

    mean_ = statistics.fmean(x_with_nan)
    print('built-in python f w/nan: ', mean_)

    mean_ = statistics.mean(x)
    print('built-in python: ', mean_)

    mean_ = np.mean(y)
    print('np mean: ', mean_)

    mean_ = statistics.mean(x)
    print('built-in python: ', mean_)

    mean_ = y.mean()
    print('y.mean(): ', mean_)
    """
    """
    weighted mean, also called the weighted arithmetic mean or weighted average
    WARNING: nan return nan
    """
    """
    x = [8.0, 1, 2.5, 4, 28.0]
    w = [0.1, 0.2, 0.3, 0.25, 0.15]
    wmean = sum(w[i] * x[i] for i in range(len(x))) / sum(w)
    print('range wmean: ', wmean)

    wmean = sum(x_ * w_ for (x_, w_) in zip(x, w)) / sum(w)
    print('zip wmean: ', wmean)
    """
    """
    for large datasets
    """
    """
    y, z, w = np.array(x), pd.Series(x), np.array(w)
    wmean = np.average(y, weights=w)
    print('large DS: ', wmean)

    wmean = np.average(z, weights=w)
    print('large DS: ', wmean)
    """
    """
    element-wise product w * y with np.sum() or .sum()
    """
    """
    print('element-wise product: ',(w * y).sum() / w.sum())
    """
    """
    Harmonic Mean

    The harmonic mean is the reciprocal of the mean of the reciprocals of all
    items in the dataset: 𝑛 / Σᵢ(1/𝑥ᵢ),
    where 𝑖 = 1, 2, …, 𝑛
    and 𝑛 is the number of items in the dataset 𝑥.
    One variant of the pure Python implementation of the harmonic mean is this:
    """
    """
    hmean = len(x) / sum(1 / item for item in x)
    print('hmean pure: ', hmean)

    hmean = statistics.harmonic_mean(x)
    print('hmean statistics: ', hmean)
    """
    """
    WARNING: nan, o, and negatives
    """
    """
    print(statistics.harmonic_mean(x_with_nan))

    print(statistics.harmonic_mean([1, 0, 2]))
    
    #print(statistics.harmonic_mean([1, 2, -2]))  # Raises StatisticsError

    print(scipy.stats.hmean(y))

    print(scipy.stats.hmean(z))
    """
    """
    Geometric Mean

    The geometric mean is the 𝑛-th root of the product of all 𝑛 elements 𝑥ᵢ
    in a dataset 𝑥: ⁿ√(Πᵢ𝑥ᵢ),
    where 𝑖 = 1, 2, …, 𝑛.
    """
    """
    gmean = 1
    for item in x:
        gmean *= item

    gmean **= 1 / len(x)
    print('gmean: ', gmean)
    """
    """
    Median

    The sample median is the middle element of a sorted dataset.
    """
    """
    n = len(x)
    if n % 2:
        median_ = sorted(x)[round(0.5*(n-1))]
    else:
        x_ord, index = sorted(x), round(0.5 * n)
        median_ = 0.5 * (x_ord[index-1] + x_ord[index])

    print('median: ', median_)

    median_ = statistics.median(x)
    print('statistics median: ', median_)

    median_ = statistics.median(x[:-1])
    print('statistics median -1: ', median_)
    """

    """
    Mode

    The sample mode is the value in the dataset that occurs most frequently.
    """
    """
    # u = [2, 3, 2, 8, 12]
    u = [2, 3, 2, 8, 12, 0, 1, 8, 1]
    mode_ = max((u.count(item), item) for item in set(u))[1]
    print('pure mode: ', mode_)

    mode_ = statistics.mode(u)
    print('statistics mode: ', mode_)
    mode_ = statistics.multimode(u)
    print('statistics multimode: ', mode_)

    v = [12, 15, 12, 15, 21, 15, 12]
    print(statistics.mode(v))  # Raises StatisticsError
    print(statistics.multimode(v))
    """
    """
    Variance
    """
    n = len(x)
    mean_ = sum(x) / n
    var_ = sum((item - mean_)**2 for item in x) / (n - 1)
    print('pure var: ', var_)

    var_ = statistics.variance(x)
    print('statistics var: ', var_)

    # Throws error
    #print('statistics var w/nan:', statistics.variance(x_with_nan))

    print('np var: ', np.var(y, ddof=1))
    print('y.var: ', y.var(ddof=1))

    print('np var: ', np.var(y_with_nan, ddof=1))
    print('y.var: ', y_with_nan.var(ddof=1))
    
    print('np nan var: ', np.nanvar(y_with_nan, ddof=1))

    print('z.var: ', z.var(ddof=1))
    print('z_with_nan.var: ', z_with_nan.var(ddof=1))

    """
    Standard Deviation
    """
    std_ = var_ ** 0.5
    print('pure std dev: ', std_)

    print('statistics.stdev: ', statistics.stdev(x))
    print('np.std(y, ddof=1): ', np.std(y, ddof=1))
    print('y.std(ddof=1): ', y.std(ddof=1))

    print('np.std(y_with_nan, ddof=1): ', np.std(y_with_nan, ddof=1))
    print('y_with_nan.std(ddof=1): ', y_with_nan.std(ddof=1))

    print('np.nanstd(y_with_nan, ddof=1): ', np.nanstd(y_with_nan, ddof=1))

    print('z.std(ddof=1): ', z.std(ddof=1))
    print('z_with_nan.std(ddof=1): ', z_with_nan.std(ddof=1))
