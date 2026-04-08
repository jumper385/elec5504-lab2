import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def lvdac2pd(lvdac_filepath, start_line=4):
    """
    Parse an LVDAC exported .txt file into a pandas DataFrame.

    The file format has 3 header rows (channel names, signal types, units)
    followed by tab-separated numeric data. The first column is time in ms.

    Data Snippet from Line 5

                Ch1		Ch2		Ch3		Ch4		Ch5		Ch6		Ch7		Ch8		
    Time 		E1		E2		AI1		AI2		AI3		AI4		AI5		AI6		
    (ms)		(V)		(V)		(V)		(V)		(V)		(V)		(V)		(V)		
    0.000		0.4		-161.5		0.01		0.02		3.69		3.69		0.01		0.02		
    0.098		5.6		-161.1		0.01		0.01		3.69		0.02		3.69		0.01		
    0.195		6.5		-164.6		0.01		0.02		3.70		0.02		3.69		0.01	

    The first three lines of the file are header information. The first line contains the channel names, the second line contains the signal types, and the third line contains the units. The data starts from the fourth line.

    Example
    -------
    >>> df = lvdac2pd('dataset/q18 FA 0.txt')
    >>> time = df['Time']
    >>> voltage = df['E1']
    """
    # check if file exists first
    if not os.path.exists(lvdac_filepath):
        raise FileNotFoundError(f"File {lvdac_filepath} not found.")

    file_lines = []
    # read the file into a pandas dataframe
    with open(lvdac_filepath, 'r') as f:
        # read lines
        file_lines = f.readlines()
        if start_line:
            file_lines = file_lines[start_line:]
        else:
            file_lines = file_lines[4:]

    # clean lines; remove \t; split them if they exist
    file_lines = [line.strip().split('\t') for line in file_lines]
    file_lines = [[item for item in line if item] for line in file_lines]
    col_names = [x.strip() for x in file_lines[1]]
    file_lines = [[float(x) for x in line] for line in file_lines[3:]]

    df = pd.DataFrame(file_lines, columns=col_names)

    return df

def calculate_average_voltage(time_series, voltage_series):
    """
    Compute the average (mean) voltage over a time interval using trapezoidal integration.

    Method
    ------
    The average voltage is defined as the integral of v(t) over the interval [t0, t1]
    divided by the length of that interval:

        Vavg = (1 / (t1 - t0)) * integral_{t0}^{t1} v(t) dt

    The integral is evaluated numerically using the trapezoidal rule via np.trapezoid.

    Parameters
    ----------
    time_series : pd.Series
        Time values in ms.
    voltage_series : pd.Series
        Voltage values in V, aligned with time_series.

    Returns
    -------
    float
        Average voltage in V.

    Example
    -------
    >>> df = lvdac2pd('dataset/q18 FA 0.txt')
    >>> avg = calculate_average_voltage(df['Time'], df['E1'])
    """
    timespan = time_series.iloc[-1] - time_series.iloc[0]
    return (1/timespan) * np.trapezoid((voltage_series), time_series)

def calculate_rms_voltage(time_series, voltage_series):
    """
    Compute the RMS voltage over a time interval using trapezoidal integration.

    Method
    ------
    The RMS voltage is the square root of the mean of the squared voltage over [t0, t1]:

        Vrms = sqrt( (1 / (t1 - t0)) * integral_{t0}^{t1} v(t)^2 dt )

    The integral of v(t)^2 is evaluated numerically using np.trapezoid.

    Parameters
    ----------
    time_series : pd.Series
        Time values in ms.
    voltage_series : pd.Series
        Voltage values in V, aligned with time_series.

    Returns
    -------
    float
        RMS voltage in V.

    Example
    -------
    >>> df = lvdac2pd('dataset/q18 FA 0.txt')
    >>> rms = calculate_rms_voltage(df['Time'], df['E1'])
    """
    timespan = time_series.iloc[-1] - time_series.iloc[0]
    return np.sqrt((1/timespan) * np.trapezoid((voltage_series)**2, time_series))

def calculate_ripple_rms(time_series, voltage_series):
    """
    Compute the ripple RMS voltage, i.e. the RMS of the AC component of the signal.

    Method
    ------
    Any signal v(t) can be decomposed into a DC component (Vavg) and an AC ripple r(t):

        v(t) = Vavg + r(t)

    The RMS of the ripple follows from the identity:

        Vrms^2 = Vavg^2 + Vripple^2

    Rearranging:

        Vripple = sqrt( Vrms^2 - Vavg^2 )

    Vavg and Vrms are computed via calculate_average_voltage and calculate_rms_voltage
    respectively, both using trapezoidal integration.

    Parameters
    ----------
    time_series : pd.Series
        Time values in ms.
    voltage_series : pd.Series
        Voltage values in V, aligned with time_series.

    Returns
    -------
    float
        Ripple RMS voltage in V.

    Example
    -------
    >>> df = lvdac2pd('dataset/q18 FA 0.txt')
    >>> ripple = calculate_ripple_rms(df['Time'], df['E1'])
    """
    # get time difference to average between 

    mean_voltage = calculate_average_voltage(time_series, voltage_series)
    ripple_rms = calculate_rms_voltage(time_series, voltage_series)

    print(mean_voltage, ripple_rms)

    return np.sqrt(ripple_rms**2 - mean_voltage**2)

def calculate_frequency(time_series, voltage_series, smooth_window=10):
    """
    Estimate the frequency of a periodic waveform by counting rising-edge crossings
    above the mean voltage.

    Method
    ------
    1. The waveform is smoothed with a centred rolling mean of width `smooth_window`
       to suppress high-frequency noise.
    2. A boolean mask flags samples above the signal mean.
    3. Rising edges are identified as transitions from below-mean to above-mean
       (i.e. consecutive samples where mask[i-1]=False and mask[i]=True).
    4. The number of rising edges equals the number of complete cycles N.
    5. Frequency is then:

           f = N / T_total

       where T_total = (t_last - t_first) converted from ms to seconds.

    Parameters
    ----------
    time_series : pd.Series
        Time values in ms.
    voltage_series : pd.Series
        Voltage values in V, aligned with time_series.
    smooth_window : int, optional
        Rolling average window size to reduce noise before edge detection (default 10).

    Returns
    -------
    float
        Estimated frequency in Hz.

    Example
    -------
    >>> df = lvdac2pd('dataset/q18 FA 0.txt')
    >>> freq = calculate_frequency(df['Time'], df['E1'])
    >>> freq = calculate_frequency(df['Time'], df['E1'], smooth_window=5)
    """

    # smooth waveform
    voltage_series = voltage_series.rolling(window=smooth_window, center=True).mean()

    # count number of rising edges above average voltage
    mean_voltage = np.mean(voltage_series)

    above_mean = voltage_series > mean_voltage

    # find start of contiguous segments of above_mean
    rising_edges = np.where((above_mean[1:].values) & (~above_mean[:-1].values))[0] + 1

    num_cycles = len(rising_edges)
    total_time = time_series.iloc[-1] - time_series.iloc[0]
    frequency = num_cycles / (total_time / 1000)  # convert ms to seconds

    return frequency