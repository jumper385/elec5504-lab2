import os
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import *

HEADLESS_MODE=True

OUTPUT_DIR = "output_average-voltage"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def question_29():
    df = pd.read_csv("dataset/table2.tsv", sep="\t")
    
    firing_angle = df['fa']
    eb_theory = df['theory']
    eb_r = df['eb_r']
    eb_rl = df['eb_rl']

    fig, ax = plt.subplots(1, figsize=(9, 3))
    ax.plot(firing_angle, eb_theory, label="Theoretical Average Voltage", marker='o', c='black', lw=0.5, markersize=2)
    ax.plot(firing_angle, eb_r, label="Average Voltage with R Load", marker='o', c='blue', lw=0.5, markersize=2)
    # ax.plot(firing_angle, eb_rl, label="Average Voltage with RL Load", marker='o', c='red', lw=0.5, markersize=2)
    ax.set_xlabel("Firing Angle (Degrees)")
    ax.set_ylabel("Average Voltage (V)")
    ax.set_title("Average Voltage vs Firing Angle")
    ax.legend()

    # display midline
    ax.axhline(0, color='gray', lw=0.5, ls='--')

    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "q29.png"), dpi=300)

    if not HEADLESS_MODE:
        plt.show()

def question_37():
    filepath = "dataset/q37 fa78_5.txt"

    df = lvdac2pd(filepath)

    time = df["Time"]
    voltage = df["E3"]
    current = df["I3"]

    fig, ax = plt.subplots(1, 2, sharex=True, figsize=(9, 3))
    ax[0].set_title("E3 Voltage @ FA=78.5 Degrees")
    ax[0].plot(time, voltage, label="E3", color='black', linewidth=0.5)
    ax[0].set_ylabel("E3 (V)")
    ax[0].legend()

    ax[1].set_title("I3 Current @ FA=78.5 Degrees")
    ax[1].plot(time, current, label="I3", color='red', linewidth=0.5)
    ax[1].set_xlabel("Time (ms)")
    ax[1].set_ylabel("I3 (A)")
    ax[1].legend()

    fig.tight_layout()

    v_ave = calculate_average_voltage(time, voltage)
    i_ave = calculate_average_voltage(time, current)
    p_ave = v_ave * i_ave

    print(f"Average Voltage: {v_ave:.5f} V")
    print(f"Average Current: {i_ave:.5f} A")
    print(f"Average Power: {p_ave:.5f} W")

    plt.savefig(os.path.join(OUTPUT_DIR, "q37.png"), dpi=300)
    if not HEADLESS_MODE:
        plt.show()

def question_40():
    df = pd.read_csv("dataset/table2.tsv", sep="\t")
    
    firing_angle = df['fa']
    eb_theory = df['theory']
    eb_r = df['eb_r']
    eb_rl = df['eb_rl']

    fig, ax = plt.subplots(1, figsize=(9, 3))
    ax.plot(firing_angle, eb_theory, label="Theoretical Average Voltage", marker='o', c='black', lw=0.5, markersize=2)
    # ax.plot(firing_angle, eb_r, label="Average Voltage with R Load", marker='o', c='blue', lw=0.5, markersize=2)
    ax.plot(firing_angle, eb_rl, label="Average Voltage with RL Load", marker='o', c='red', lw=0.5, markersize=2)
    ax.set_xlabel("Firing Angle (Degrees)")
    ax.set_ylabel("Average Voltage (V)")
    ax.set_title("Average Voltage vs Firing Angle")
    ax.legend()

    # display midline
    ax.axhline(0, color='gray', lw=0.5, ls='--')

    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "q40.png"), dpi=300)

    if not HEADLESS_MODE:
        plt.show()    

def main():
    question_29()
    question_37()
    question_40()

if __name__ == "__main__":
    main()