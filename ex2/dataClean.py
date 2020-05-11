import pandas as pd

filePath = "PriceFull7290696200003-097-202005040319-001.csv"
table = pd.read_csv(filePath)
print(table.isna())



