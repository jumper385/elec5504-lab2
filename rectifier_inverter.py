import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.utils import *

HEADLESS_MODE = True

OUTPUT_DIR = "output_rectifier-inverter"
figsize = (9,4)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def question_49():
    filepath_list = [
        ("dataset/q49 fa0.txt", "FA=0 Degrees"),
        ("dataset/q49 fa30.txt", "FA=30 Degrees"),
        ("dataset/q49 fa60.txt", "FA=60 Degrees"),
        ("dataset/q49 fa90.txt", "FA=90 Degrees"),
    ]

    fig, ax = plt.subplots(2, len(filepath_list), sharex=True, sharey='row', figsize=figsize)

    for filepath, label in filepath_list:
        df = lvdac2pd(filepath)
        time = df["Time"]
        voltage = df["E3"]
        current = df["I3"]

        ax[0, filepath_list.index((filepath, label))].set_title(f"{label}")
        ax[0, filepath_list.index((filepath, label))].plot(time, voltage, label="E3", color='black', linewidth=0.5)
        ax[0, filepath_list.index((filepath, label))].set_ylabel("E3 (V)")
        ax[0, filepath_list.index((filepath, label))].legend()
        ax[0, filepath_list.index((filepath, label))].axhline(0, color='gray', lw=0.5, ls='--')

        ax[1, filepath_list.index((filepath, label))].plot(time, current, label="I3", color='red', linewidth=0.5)
        ax[1, filepath_list.index((filepath, label))].set_xlabel("Time (ms)")
        ax[1, filepath_list.index((filepath, label))].set_ylabel("I3 (A)")
        ax[1, filepath_list.index((filepath, label))].set_ylim(0, 3)
        ax[1, filepath_list.index((filepath, label))].legend()

        # print average voltage and current
        v_ave = calculate_average_voltage(time, voltage)
        i_ave = calculate_average_voltage(time, current)
        p_ave = v_ave * i_ave
        print(f"{label}: Average Voltage = {v_ave:.5f} V, Average Current = {i_ave:.5f} A", f"Average Power = {p_ave:.5f} W")

    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "q49.png"), dpi=300)

    if not HEADLESS_MODE:
        plt.show()

def question_55():
    filepath = "dataset/table3.tsv"
    df = pd.read_csv(filepath, sep="\t")
    df_theory = pd.read_csv("dataset/table2.tsv", sep="\t")
    
    print(df)

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.plot(df_theory["fa"], df_theory["theory"], label="Theoretical Average Voltage", marker='o', c='grey', lw=0.5, markersize=2, ls='--')
    ax.plot(df["fa"], df["eb_avg"], label="Average Voltage", marker='o', c='blue', lw=0.5, markersize=2)
    ax.set_xlabel("Firing Angle (Degrees)")
    ax.set_ylabel("Average Voltage (V)")
    ax.set_title("Average Voltage vs Firing Angle")
    ax.hlines(0, 0, 180, color='gray', lw=0.5, ls='--')  # midline
    ax.legend()

    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "q55.png"), dpi=300)

    if not HEADLESS_MODE:
        plt.show()

def question_56():
    filepath = "dataset/table3.tsv"

    df = pd.read_csv(filepath, sep="\t")

    output_power = df["pout_w"]
    input_active_power = df["pin_active"]
    input_reactive_power = df["pin_reactive"]

    # print out power curves
    fig, ax = plt.subplots(1, figsize=figsize)
    # triangle for output power
    ax.plot(df["fa"], output_power, label="Output Power (W)", marker="^", c='black', lw=0.5, markersize=2)

    # same marker for input active and reactive power
    ax.plot(df["fa"], input_active_power, label="Input Active Power (W)", marker='o', c='blue', lw=0.5, markersize=2)
    ax.plot(df["fa"], input_reactive_power, label="Input Reactive Power (Var)", marker='o', c='red', lw=0.5, markersize=2)
    ax.set_xlabel("Firing Angle (Degrees)")
    ax.set_ylabel("Power (W/Var)")
    ax.set_title("Input and Output Power vs Firing Angle")
    ax.hlines(0, 0, 180, color='gray', lw=0.5, ls='--')  # midline
    ax.legend()

    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "q56.png"), dpi=300)

    if not HEADLESS_MODE:
        plt.show()

def main():
    question_49()
    question_55()
    question_56()

if __name__ == "__main__":
    main()
