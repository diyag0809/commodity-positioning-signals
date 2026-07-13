import pandas as pd
import matplotlib.pyplot as plt

merged = pd.read_csv('data/merged_signal_returns.csv', parse_dates=['Report_Date_as_YYYY-MM-DD'])
merged = merged.sort_values('Report_Date_as_YYYY-MM-DD')

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

commodities = ['CORN - CHICAGO BOARD OF TRADE', 'GOLD - COMMODITY EXCHANGE INC.']

for ax, commodity in zip(axes, commodities):
    subset = merged[merged['Market_and_Exchange_Names'] == commodity]
    ax.plot(subset['Report_Date_as_YYYY-MM-DD'], subset['zscore'])
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    midpoint = merged['Report_Date_as_YYYY-MM-DD'].median()
    ax.axvline(midpoint, color='red', linestyle='--', linewidth=0.8, label='Walk-forward split')
    ax.set_title(f"{commodity.split(' - ')[0]}: Managed Money Positioning Z-Score")
    ax.set_ylabel('Z-score')
    ax.legend()

plt.tight_layout()
plt.savefig('charts/zscore_over_time.png', dpi=150)
print("Saved chart to charts/zscore_over_time.png")
correlations = {
    'Corn': -0.0783,
    'Natural Gas': 0.0079,
    'Crude Oil': 0.0019,
    'Gold': -0.0864
}

significant = {
    'Corn': True,
    'Natural Gas': False,
    'Crude Oil': False,
    'Gold': True
}

fig2, ax2 = plt.subplots(figsize=(8, 5))
colors = ['#d62728' if significant[c] else '#7f7f7f' for c in correlations]
ax2.bar(correlations.keys(), correlations.values(), color=colors)
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_ylabel('Correlation (z-score vs 4-week forward return)')
ax2.set_title('Positioning-Return Correlation by Commodity\n(red = statistically significant, p < 0.05)')
plt.tight_layout()
plt.savefig('charts/correlation_comparison.png', dpi=150)
print("Saved second chart to charts/correlation_comparison.png")