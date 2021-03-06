import pandas as pd

df = pd.read_csv("parks_events_data.csv")
tmp_df = pd.DataFrame()

for index in df.index:
    categories = df.ix[index]["categories"]
    categories = categories.replace("free","").replace("Free","").replace("FREE","")
    tmp_dicter = df.ix[index].to_dict()
    tmp_dicter["categories"] = categories
    tmp_df = tmp_df.append(tmp_dicter, ignore_index=True)

tmp_df.to_csv("parks_events_data_updated.csv", index = False)
