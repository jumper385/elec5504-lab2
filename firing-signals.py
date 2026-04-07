import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.utils import *

HEADLESS=False
OUTPUT_DIR = "output_firing_signals"
figsize = (9,4)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def question_19():
    src_filepath = "dataset/q18 FA 0.txt"
    filename = os.path.basename(src_filepath).replace(".txt", ".png")
    print(filename)
    dest_filepath = f"{OUTPUT_DIR}/{filename}"

    file = lvdac2pd(src_filepath)

    time = file["Time"]

    e1 = file["E1"]
    e2 = file["E2"]

    ai1 = file["AI1"]
    ai2 = file["AI2"]
    ai3 = file["AI3"]
    ai4 = file["AI4"]
    ai5 = file["AI5"]
    ai6 = file["AI6"]

    fig, ax = plt.subplots(2, sharex=True, figsize=figsize)

    ax[0].set_title("V_LL vs Firing Signals (0 Degree Firing Angle)")
    ax[0].plot(time, e1, label="E1", color='black', linewidth=0.5)
    ax[0].plot(time, e2, label="E2", color='red', linewidth=0.5)
    ax[0].set_ylabel("Line to Line Voltage (V)")
    ax[0].legend(loc="upper right")

    # plot them one onto another
    increment = 5
    ax[1].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
    ax[1].plot(time, ai2 + increment, label="AI2", color='orange', linewidth=0.5)
    ax[1].plot(time, ai3 + 2 * increment, label="AI3", color='green', linewidth=0.5)
    ax[1].plot(time, ai4 + 3 * increment, label="AI4", color='purple', linewidth=0.5)
    ax[1].plot(time, ai5 + 4 * increment, label="AI5", color='brown', linewidth=0.5)
    ax[1].plot(time, ai6 + 5 * increment, label="AI6", color='pink', linewidth=0.5)

    # turn off y axis for the second subplot
    # ax[1].yaxis.set_visible(False)
    ax[1].set_xlabel("Time (ms)")
    ax[1].set_ylabel("Firing Signals (AI1-AI6)")
    ax[1].legend(loc="upper right")

    fig.tight_layout()
    plt.savefig(dest_filepath, dpi=300)

    if not HEADLESS:
        plt.show()

def question_20():
    file_list = [
        ("dataset/q20 FA 0.txt", "FA=0 Degrees"),
        ("dataset/q20 FA 30.txt", "FA=30 Degrees"),
        ("dataset/q20 FA 60.txt", "FA=60 Degrees"),
        ("dataset/q20 FA 90.txt", "FA=90 Degrees")
    ]

    fig, ax = plt.subplots(2, len(file_list), sharex=True, figsize=figsize, sharey="row")

    for file, label in file_list:
        filename = os.path.basename(file).replace(".txt", ".png")
        print(filename)
        dest_filepath = f"{OUTPUT_DIR}/{filename}"

        data = lvdac2pd(file)

        time = data["Time"]

        e1 = data["E1"]
        e3 = data["E3"]

        # average calculation
        e3_avg = calculate_average_voltage(time, e3)
        e3_rms = calculate_rms_voltage(time, e3)
        e1_rms = calculate_rms_voltage(time, e1)

        e3_ripple_rms = calculate_ripple_rms(time, e3)

        print(e1_rms, e3_rms, e3_avg)
        print(f"{label} - Ripple RMS Voltage: {e3_ripple_rms:.5f} V")

        ai1 = data["AI1"]
        ai2 = data["AI2"]
        ai3 = data["AI3"]
        ai4 = data["AI4"]
        ai5 = data["AI5"]
        ai6 = data["AI6"]

        ax[0][file_list.index((file, label))].set_title(f"{label}")
        ax[0][file_list.index((file, label))].plot(time, e1, label="E1", color='black', linewidth=0.5)
        ax[0][file_list.index((file, label))].plot(time, e3, label="E3", color='red', linewidth=0.5)
        ax[0][0].set_ylabel("Line to Line Voltage (V)")
        ax[0][0].legend()

        increment = 5
        ax[1][file_list.index((file, label))].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
        ax[1][file_list.index((file, label))].plot(time, ai2 + increment, label="AI2", color='orange', linewidth=0.5)
        ax[1][file_list.index((file, label))].plot(time, ai3 + 2 * increment, label="AI3", color='green', linewidth=0.5)
        ax[1][file_list.index((file, label))].plot(time, ai4 + 3 * increment, label="AI4", color='purple', linewidth=0.5)
        ax[1][file_list.index((file, label))].plot(time, ai5 + 4 * increment, label="AI5", color='brown', linewidth=0.5)
        ax[1][file_list.index((file, label))].plot(time, ai6 + 5 * increment, label="AI6", color='pink', linewidth=0.5)
        ax[1][0].set_xlabel("Time (ms)")
        ax[1][0].set_ylabel("Firing Signals (AI1-AI6)")
        ax[1][0].legend()

    fig.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/q20_all.png", dpi=300)

    if not HEADLESS:
        plt.show()

def question_22():
    filepath = "dataset/q22 fa0.txt"
    filename = os.path.basename(filepath).replace(".txt", ".png")
    print(filename)
    dest_filepath = f"{OUTPUT_DIR}/{filename}"

    data = lvdac2pd(filepath)
    time = data["Time"]
    e1 = data["E1"]
    e2 = data["E2"]

    ai5 = data["AI5"]
    ai1 = data["AI1"]
    ai2 = data["AI2"]
    ai6 = data["AI6"]

    i3 = data["I3"]
    e3 = data["E3"]

    fig, ax = plt.subplots(2,3, sharex=True, figsize=(9, 4))
    ax[0][0].set_title("V_LL vs Firing Signals")
    ax[0][0].plot(time, e1, label="E1", color='black', linewidth=0.5)
    ax[0][0].plot(time, e2, label="E2", color='red', linewidth=0.5)
    ax[0][0].set_ylabel("V_LL (V)")
    ax[0][1].set_ylim(-200, 200)

    increment = 5
    ax[1][0].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
    ax[1][0].plot(time, ai2 + increment, label="AI2", color='orange', linewidth=0.5)
    ax[1][0].plot(time, ai5 + 2 * increment, label="AI5", color='green', linewidth=0.5)
    ax[1][0].plot(time, ai6 + 3 * increment, label="AI6", color='purple', linewidth=0.5)
    ax[1][0].set_xlabel("Time (ms)")
    # top right corner
    ax[1][0].legend(loc="upper right")

    ax[1][0].set_ylabel("Firing Signal")
    ax[0][1].plot(time, e3, label="E3", color='black', linewidth=0.5)
    ax[0][1].set_title("Load Voltage")
    ax[0][1].set_ylim(0, 200)
    ax[0][1].set_ylabel("E3 (V)")

    ax[1][1].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
    ax[1][1].plot(time, ai2 + increment, label="AI2", color='orange', linewidth=0.5)
    ax[1][1].plot(time, ai5 + 2 * increment, label="AI5", color='green', linewidth=0.5)
    ax[1][1].plot(time, ai6 + 3 * increment, label="AI6", color='purple', linewidth=0.5)
    ax[1][1].set_xlabel("Time (ms)")

    ax[0][2].plot(time, i3, label="I3", color='black', linewidth=0.5)
    ax[0][2].set_title("Load Current")
    ax[0][2].set_ylabel("I3 (A)")
    ax[0][2].set_ylim(0, 1)
    ax[0][2].legend()

    ax[1][2].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
    ax[1][2].plot(time, ai2 + increment, label="AI2", color='orange', linewidth=0.5)
    ax[1][2].plot(time, ai5 + 2 * increment, label="AI5", color='green', linewidth=0.5)
    ax[1][2].plot(time, ai6 + 3 * increment, label="AI6", color='purple', linewidth=0.5)
    ax[1][2].set_xlabel("Time (ms)")

    fig.tight_layout()
    plt.savefig(dest_filepath, dpi=300)

    if not HEADLESS:
        plt.show()

def question_24():
    file_list = [
        ("dataset/q24 fa0.txt", "FA=0 Degrees"),
        ("dataset/q24 fa20.txt", "FA=20 Degrees"),
        ("dataset/q24 fa30.txt", "FA=30 Degrees"), 
        ("dataset/q24 fa60.txt", "FA=60 Degrees"),
    ]

    fig, ax = plt.subplots(3, len(file_list), sharex=True, figsize=(9, 6), sharey="row")
    for file, label in file_list:
        filename = os.path.basename(file).replace(".txt", ".png")
        print(filename)
        dest_filepath = f"{OUTPUT_DIR}/{filename}"

        data = lvdac2pd(file)

        time = data["Time"]

        e1 = data["E1"]
        e2 = data["E2"]

        ai5 = data["AI5"]
        ai1 = data["AI1"]
        ai2 = data["AI2"]
        ai6 = data["AI6"]

        e3 = data["E3"]
        i3 = data["I3"]


        # plot firing signals
        ax[2][file_list.index((file, label))].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
        ax[2][file_list.index((file, label))].plot(time, ai2 + 5, label="AI2", color='orange', linewidth=0.5)
        ax[2][file_list.index((file, label))].plot(time, ai5 + 10, label="AI5", color='green', linewidth=0.5)
        ax[2][file_list.index((file, label))].plot(time, ai6 + 15, label="AI6", color='purple', linewidth=0.5)
        ax[2][0].set_xlabel("Time (ms)")
        ax[2][0].set_ylabel("Firing Signals")
        ax[2][0].set_xlim(3, 30)
        ax[2][0].legend()

        # plot output current
        ax[1][file_list.index((file, label))].plot(time, i3, label="I3", color='red', linewidth=0.5)
        ax[1][0].set_xlabel("Time (ms)")
        ax[1][0].set_ylabel("I3 (A)")
        ax[1][0].set_ylim(0, 1)
        ax[1][0].legend()

        # plot output voltage e3
        ax[0][file_list.index((file, label))].set_title(f"{label}")
        ax[0][file_list.index((file, label))].plot(time, e3, label="E3", color='black', linewidth=0.5)
        ax[0][0].set_ylabel("E3 (V)")
        ax[0][0].legend()

        # calculate average current and voltage output
        print(f"{label} - Average Voltage: {calculate_average_voltage(time, e3)} V")
        print(f"{label} - Average Current: {calculate_average_voltage(time, i3)} A")

    fig.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/q24_all.png", dpi=300)

    if not HEADLESS:
        plt.show()

def question_25():
    file_list = [
        ("dataset/q25 fa 80.txt", "FA=80 Degrees"),
        ("dataset/q25 fa 90.txt", "FA=90 Degrees"),
    ]

    fig, ax = plt.subplots(3, len(file_list), sharex=True, figsize=(9, 6), sharey="row")
    for file, label in file_list:
        filename = os.path.basename(file).replace(".txt", ".png")
        print(filename)
        dest_filepath = f"{OUTPUT_DIR}/{filename}"

        data = lvdac2pd(file)

        time = data["Time"]

        e1 = data["E1"]
        e2 = data["E2"]

        ai5 = data["AI5"]
        ai1 = data["AI1"]
        ai2 = data["AI2"]
        ai6 = data["AI6"]

        e3 = data["E3"]
        i3 = data["I3"]

        # plot firing signals
        ax[2][file_list.index((file, label))].plot(time, ai1, label="AI1", color='blue', linewidth=0.5)
        ax[2][file_list.index((file, label))].plot(time, ai2 + 5, label="AI2", color='orange', linewidth=0.5)
        ax[2][file_list.index((file, label))].plot(time, ai5 + 10, label="AI5", color='green', linewidth=0.5)
        ax[2][file_list.index((file, label))].plot(time, ai6 + 15, label="AI6", color='purple', linewidth=0.5)
        ax[2][0].set_xlabel("Time (ms)")
        ax[2][0].set_ylabel("Firing Signals")
        ax[2][0].legend()

        # plot output current
        ax[1][file_list.index((file, label))].plot(time, i3, label="I3", color='red', linewidth=0.5)
        ax[1][0].set_xlabel("Time (ms)")
        ax[1][0].set_ylabel("I3 (A)")
        ax[1][0].set_ylim(-0.5, 1)
        ax[1][0].legend()

        # plot output voltage e3
        ax[0][file_list.index((file, label))].set_title(f"{label}")
        ax[0][file_list.index((file, label))].plot(time, e3, label="E3", color='black', linewidth=0.5)
        ax[0][0].set_ylabel("E3 (V)")
        ax[0][0].legend()

        # calculate average current and voltage output
        print(f"{label} - Average Voltage: {calculate_average_voltage(time, e3)} V")
        print(f"{label} - Average Current: {calculate_average_voltage(time, i3)} A")

    fig.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/q25_all.png", dpi=300)

    if not HEADLESS:
        plt.show()

def main():
    question_19()
    question_20()
    question_22()
    question_24()
    question_25()

if __name__ == "__main__":
    main()