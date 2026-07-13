import pandas as pd

cot_data = pd.read_csv('data/cot_filtered.csv')

cot_data['net_managed_money'] = cot_data['M_Money_Positions_Long_All'] - cot_data['M_Money_Positions_Short_All']

cot_data['zscore'] = cot_data.groupby('Market_and_Exchange_Names')['net_managed_money'].transform(
    lambda x: (x - x.rolling(window=104, min_periods=52).mean()) / x.rolling(window=104, min_periods=52).std()
)

print(cot_data[['Market_and_Exchange_Names', 'Report_Date_as_YYYY-MM-DD', 'net_managed_money', 'zscore']].dropna().head(10))
cot_data.to_csv('data/cot_with_signal.csv', index=False)
print("Saved signal data to data/cot_with_signal.csv")