from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from master_thesis import figure_path

data_dir = Path(__file__).parent / "phase_acceptance_data"

df_std_on, df_std_off, df_v3_on, df_v3_off, df_ua_1, df_ua_2, df_std_ba, df_v4_ba = map(
    lambda path: pd.read_csv(data_dir / path, sep="\t"),
    [
        "20190507_PhaseAcceptanceStdUserPSFon.dat",
        "20190507_PhaseAcceptanceStdUserPSFoff.dat",
        "20190507_PhaseAcceptance_Q5T2off_V3min_PSFon.dat",
        "20190507_PhaseAcceptance_Q5T2off_V3min_PSFoff.dat",
        "20190621_PhaseAcceptance_UserAcceptanceTestNo1.dat",
        "20190621_PhaseAcceptance_UserAcceptanceTestNo2.dat",
        "20170904_Q5T2off_StandardOptik_PhaseAccScan.dat",
        "20170904_Q5T2off_V4neuHarmOptimiert_No2_PhaseAccScan.dat",
    ],
)

phase = "PAHB:sDelay [ns]"
efficiency = "TOPUP1T5G:rdEffBoostRraw []"

# Q5T2off vs std user MA
fig, ax1 = plt.subplots(figsize=(9, 5))

ax1.plot(
    df_std_off[phase][137:560],
    df_std_off[efficiency][137:560],
    label="Standard User",
)
ax1.plot(
    df_v3_off[phase][137:560],
    df_v3_off[efficiency][137:560],
    label="Q5T2off",
)

ax1.legend(loc="lower right")
ax1.set_xlim(0, 2)
ax1.set_ylim(-0.1, 1.1)
ax1.set_xlabel("Phase between booster synchrotron and storage ring / ns")
ax1.set_ylabel("Injection Efficiency")
fig.tight_layout()
fig.savefig(figure_path / "phase_acceptance_q5t2off.svg")

# MA vs BA
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(9, 7))

ax1.plot(
    df_std_off[phase][137:560],
    df_std_off[efficiency][137:560],
    label="Standard User",
)
ax1.plot(
    df_v3_off[phase][137:560],
    df_v3_off[efficiency][137:560],
    label="Q5T2off",
)

ax2.plot(
    df_std_ba[phase][75:500],
    df_std_ba[efficiency][75:500],
    label="Standard User (Bachelor)",
)
ax2.plot(
    df_v4_ba[phase][136:990],
    df_v4_ba[efficiency][136:990],
    label="Q5T2off (Bachelor)",
)

ax1.legend(loc="lower right")
ax1.set_xlim(0, 2)
ax1.set_ylim(-0.1, 1.1)
ax1.set_ylabel("Injection Efficiency")
ax2.legend(loc="lower right")
ax2.set_xlim(0, 2)
ax2.set_ylim(-0.1, 1.1)
ax2.set_xlabel("Phase between booster synchrotron and storage ring / ns")
ax2.set_ylabel("Injection Efficiency")

fig.tight_layout()
fig.savefig(figure_path / "phase_acceptance_q5t2off_vs_ba.svg")
