import os
import numpy as np
import pandas as pd

def lvdac2pd(lvdac_filepath, start_line=4):
    """
    Data Snippet from Line 5

                Ch1		Ch2		Ch3		Ch4		Ch5		Ch6		Ch7		Ch8		
    Time 		E1		E2		AI1		AI2		AI3		AI4		AI5		AI6		
    (ms)		(V)		(V)		(V)		(V)		(V)		(V)		(V)		(V)		
    0.000		0.4		-161.5		0.01		0.02		3.69		3.69		0.01		0.02		
    0.098		5.6		-161.1		0.01		0.01		3.69		0.02		3.69		0.01		
    0.195		6.5		-164.6		0.01		0.02		3.70		0.02		3.69		0.01	

    The first three lines of the file are header information. The first line contains the channel names, the second line contains the signal types, and the third line contains the units. The data starts from the fourth line.
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
    timespan = time_series.iloc[-1] - time_series.iloc[0]
    return (1/timespan) * np.trapezoid((voltage_series), time_series)

def calculate_rms_voltage(time_series, voltage_series):
    timespan = time_series.iloc[-1] - time_series.iloc[0]
    return np.sqrt((1/timespan) * np.trapezoid((voltage_series)**2, time_series))

def calculate_ripple_rms(time_series, voltage_series):
    # get time difference to average between 

    mean_voltage = calculate_average_voltage(time_series, voltage_series)
    ripple_rms = calculate_rms_voltage(time_series, voltage_series)

    print(mean_voltage, ripple_rms)

    return np.sqrt(ripple_rms**2 - mean_voltage**2)