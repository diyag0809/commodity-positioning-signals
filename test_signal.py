import pandas as pd

signal_data = pd.read_csv('data/cot_with_signal.csv')
price_data = pd.read_csv('data/price_data.csv', index_col='Date', parse_dates=True)

print(signal_data.shape)
print(price_data.shape)
print(price_data.head())
returns_1w = price_data.pct_change(periods=5).shift(-5)
returns_4w = price_data.pct_change(periods=20).shift(-20)

returns_1w_long = returns_1w.stack().reset_index()
returns_1w_long.columns = ['Date', 'Market_and_Exchange_Names', 'return_1w']

returns_4w_long = returns_4w.stack().reset_index()
returns_4w_long.columns = ['Date', 'Market_and_Exchange_Names', 'return_4w']

signal_data['Report_Date_as_YYYY-MM-DD'] = pd.to_datetime(signal_data['Report_Date_as_YYYY-MM-DD'])

merged = signal_data.merge(
    returns_1w_long,
    left_on=['Report_Date_as_YYYY-MM-DD', 'Market_and_Exchange_Names'],
    right_on=['Date', 'Market_and_Exchange_Names'],
    how='left'
)

merged = merged.merge(
    returns_4w_long,
    left_on=['Report_Date_as_YYYY-MM-DD', 'Market_and_Exchange_Names'],
    right_on=['Date', 'Market_and_Exchange_Names'],
    how='left'
)

print(merged[['Market_and_Exchange_Names', 'Report_Date_as_YYYY-MM-DD', 'zscore', 'return_1w', 'return_4w']].dropna().head(10))
merged.to_csv('data/merged_signal_returns.csv', index=False)
print("Saved merged data to data/merged_signal_returns.csv")
from scipy.stats import pearsonr

print("\n--- Correlation between z-score and 1-week forward return ---")
for commodity in merged['Market_and_Exchange_Names'].unique():
    subset = merged[merged['Market_and_Exchange_Names'] == commodity].dropna(subset=['zscore', 'return_1w'])
    corr, p_value = pearsonr(subset['zscore'], subset['return_1w'])
    print(f"{commodity}: correlation = {corr:.4f}, p-value = {p_value:.4f}, n = {len(subset)}")
    print("\n--- Correlation between z-score and 4-week forward return ---")
for commodity in merged['Market_and_Exchange_Names'].unique():
    subset = merged[merged['Market_and_Exchange_Names'] == commodity].dropna(subset=['zscore', 'return_4w'])
    corr, p_value = pearsonr(subset['zscore'], subset['return_4w'])
    print(f"{commodity}: correlation = {corr:.4f}, p-value = {p_value:.4f}, n = {len(subset)}")
    print("\n--- Walk-forward check: split into two halves ---")
midpoint = merged['Report_Date_as_YYYY-MM-DD'].median()
print(f"\nWalk-forward split date: {midpoint}")

for commodity in ['CORN - CHICAGO BOARD OF TRADE', 'GOLD - COMMODITY EXCHANGE INC.']:
    for label, period in [('First half', merged['Report_Date_as_YYYY-MM-DD'] <= midpoint),
                           ('Second half', merged['Report_Date_as_YYYY-MM-DD'] > midpoint)]:
        subset = merged[(merged['Market_and_Exchange_Names'] == commodity) & period].dropna(subset=['zscore', 'return_4w'])
        corr, p_value = pearsonr(subset['zscore'], subset['return_4w'])
        print(f"{commodity} ({label}): correlation = {corr:.4f}, p-value = {p_value:.4f}, n = {len(subset)}")