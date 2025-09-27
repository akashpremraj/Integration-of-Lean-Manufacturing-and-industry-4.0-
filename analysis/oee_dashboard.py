# OEE Dashboard (Synthetic Demo)
Computes Availability, Performance, Quality and OEE from `data-samples/line_production.csv`
and visualises daily trends for two lines.

import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
CSV = Path(__file__).resolve().parents[1] / 'data-samples' / 'line_production.csv'
df = pd.read_csv(CSV, parse_dates=['date'])
df.head()

ideal_rate = {"BodyShop": 0.5, "Assembly": 0.8}
df['planned_effective'] = df['planned_time_min'] - df['changeover_min']
df['availability'] = (df['run_time_min'] / df['planned_effective']).clip(upper=1)
df['performance'] = ((df['good_units'] + df['scrap_units']) /
                     (df['line'].map(ideal_rate) * df['run_time_min'])).clip(upper=1)
df['quality'] = (df['good_units'] / (df['good_units'] + df['scrap_units'])).fillna(0)
df['oee'] = df['availability'] * df['performance'] * df['quality']
df[['availability','performance','quality','oee']].describe()

for metric in ['availability','performance','quality','oee']:
    pivot = df.pivot_table(index='date', columns='line', values=metric)
    ax = pivot.plot(title=f'{metric.upper()} by line (daily)')
    ax.set_xlabel('Date'); ax.set_ylabel(metric.upper()); plt.show()

