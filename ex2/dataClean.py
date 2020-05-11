import pandas as pd

victory_price_full_1 = "PriceFull7290696200003-097-202005040319-001.csv"
t_victory_prices_full_1 = pd.read_csv(victory_price_full_1)

victory_price_full_2 = "PriceFull7290696200003-077-202005040327-001.csv"
t_victory_prices_full_2 = pd.read_csv(victory_price_full_2)

victory_promo_full_1 = "PromoFull7290696200003-097-202005040319-001.csv"
t_victory_promo_full_1 = pd.read_csv(victory_promo_full_1)

"""missing files"""
# print(t_victory_prices_full_1.isna())
# print(t_victory_prices_full_1.isnull())
# print(t_victory_promo_full_1.isna())

"""corrupted files"""
# todo: add example

"""different units"""
# print(pd.DataFrame(t_victory_promo_full_1, columns=["DiscountRate"]))
# DiscountRate = pd.DataFrame(t_victory_promo_full_1)["DiscountRate"]
# print("column name: DiscountRate\nmin value: " + str(min(DiscountRate)) +
# "\nmax value: " + str(max(DiscountRate)))

"""unrelated data"""
# Items = pd.DataFrame(t_victory_prices_full_1)["ItemName"]
# print(Items)

"""mixed string names and code names"""
# ManufactureName1 = pd.DataFrame(t_victory_prices_full_1, columns=["ItemCode", "ManufactureName"])
# ManufactureName2 = pd.DataFrame(t_victory_prices_full_2, columns=["ItemCode", "ManufactureName"])
# print(ManufactureName1.iloc[8], "\n\n", ManufactureName2.iloc[7])

"""unavailable data"""
# Manufacture = pd.DataFrame(t_victory_prices_full_2, columns=["ItemCode", "ManufactureName"])
# print(Manufacture.iloc[671])
