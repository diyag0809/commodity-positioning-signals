import cot_reports as cot
import pandas as pd
print("Starting download, this may take a minute...")

cot_data = cot.cot_all(cot_report_type='disaggregated_fut')

target_commodities = [
    'CORN - CHICAGO BOARD OF TRADE',
    'NATURAL GAS - NEW YORK MERCANTILE EXCHANGE',
    'CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE',
    'GOLD - COMMODITY EXCHANGE INC.'
]

filtered_data = cot_data[cot_data['Market_and_Exchange_Names'].isin(target_commodities)]

print(filtered_data.shape)
print(filtered_data['Market_and_Exchange_Names'].value_counts())
filtered_data.to_csv('data/cot_filtered.csv', index=False)
print("Saved filtered data to data/cot_filtered.csv")