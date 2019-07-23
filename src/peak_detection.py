import numpy as np
from scipy import stats

def thresh_alg(y, lag, threshold, influence, mode='std'):
    # Checks to see if input y is shaped as an NumPy array vector and flattens if so
    if len(y.shape) > 1:
        y = y.reshape(y.size)

    # Determines whether our peak detection algo will utilize mean/std or median/mad
    # for average/deviation calculation.
    if mode=='std':
        avg = np.mean
        dev = np.std
    elif mode=='mad':
        avg = np.median
        dev = stats.median_absolute_deviation
    else:
        raise ValueError("Invalid mode -- must either be \'std\' or \'mad\'.")
    ## Initializing our signal vector
    signals = np.zeros(len(y))
    ## Initializing our filtered series
    filteredY = np.zeros(len(y))
    filteredY[0:lag+1] = y[0:lag+1]
    ## Initialize our filters
    avgFilter = np.zeros(len(y))
    avgFilter[lag] = avg(y[0:lag+1])

    stdFilter = np.zeros(len(y))
    stdFilter[lag] = dev(y[0:lag+1])

    ## Looping over the rest of our data points in y (from y[lag+1] to y[y.size+1])
    for i in range(lag+1,y.size):
        ## Check to see if value is a threshold number of standard deviations away
        if np.abs(y[i] - avgFilter[i-1]) > threshold * stdFilter[i-1]:
            if y[i] > avgFilter[i-1]:
                ## For our case, we are only considering positive signals to signify a spike in relevancy
                ## for news-related events.
                signals[i] = 1;
            ## Making the influence lower
            ## TODO: Inplement a non-stationary transform instead
            filteredY[i] = influence * y[i] + (1-influence) * filteredY[i-1]
        else:
            ## No signal
            signals[i] = 0
            filteredY[i] = y[i]
        ## Adjusting our filters by moving our window
        avgFilter[i] = avg(filteredY[i-lag:i+1])
        stdFilter[i] = dev(filteredY[i-lag:i+1])
    return (signals, avgFilter, stdFilter)
