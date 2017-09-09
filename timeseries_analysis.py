import pandas as pd
import matplotlib.pyplot as plt


def frequency_by_day(dates):
    dates = list(dates)
    unique_dates = set(dates)
    counts = []
    for date in unique_dates:
        counts.append(dates.count(date))
    return unique_dates, counts


def get_categories(categories):
    full_categories = []
    for category in categories:
        full_categories += [elem.strip() for elem in category.split(",")]
    return list(set(full_categories))


def create_segmented_df(df, category):
    tmp_df = pd.DataFrame()
    for index in df.index:
        if category in df.ix[index]["categories"]:
            tmp_df = tmp_df.append(df.ix[index])
    return tmp_df


def segment_timeseries_by_categories(df, categories):
    segmentation = {}.fromkeys(categories)
    for category in categories:
        segmentation[category] = create_segmented_df(df, category)
    return segmentation

def plot_data(df, title):
    df["dates"] = pd.to_datetime(df["dates"])
    unique_dates, counts = frequency_by_day(df["dates"])
    date_freq = pd.Series(counts, index=unique_dates)
    date_freq.plot(title=title)
    plt.show()

df = pd.read_csv("parks_events_data.csv")
plot_data(df, "overall")
categories = get_categories(df["categories"])
segmentation = segment_timeseries_by_categories(df, categories)
for key in list(segmentation.keys()):
    plot_data(segmentation[key], key)
