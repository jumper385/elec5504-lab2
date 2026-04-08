import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.utils import *

HEADLESS_MODE = True

OUTPUT_DIR = "output_discussion"
figsize = (9,4)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def question_a():
    # calculate waveform frequency at differnet firing angles
    filepath_list = [
        ("dataset/q20 FA 0.txt", "FA=0 Degrees"),
        ("dataset/q20 FA 30.txt", "FA=30 Degrees"),
        ("dataset/q20 FA 60.txt", "FA=60 Degrees"),
        ("dataset/q20 FA 90.txt", "FA=90 Degrees"),
    ]

    for file in filepath_list:

        df = lvdac2pd(file[0])
        time = df["Time"]
        voltage = df["E3"]

        # calculate frequency
        freq = calculate_frequency(time, voltage)
        print(f"{file[1]}: Frequency = {freq:.5f} Hz")

def main():
    question_a()

if __name__ == "__main__":
    main()