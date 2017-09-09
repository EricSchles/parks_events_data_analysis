import requests
import pandas as pd
import lxml.html


def parse_date(event_link: str) -> str:
    date = event_link.split("/")[2:5]
    month = date[1]
    day = date[2]
    year = date[0]
    return month + "/" + day + "/" + year


def get_events_data(page: int):
    response = requests.get("https://www.nycgovparks.org/events/p"+str(page))
    html = lxml.html.fromstring(response.text)
    event_links = html.xpath("//h3[@class='event-title']/a/@href")
    event_titles = [elem.text_content() for elem in html.xpath("//h3[@class='event-title']/a")]
    dates = [parse_date(event_link) for event_link in event_links]
    event_links = ["https://www.nycgovparks.org"+event_link for event_link in event_links]
    categories = get_categories(html)
    return event_links, dates, event_titles, categories
    
    
def get_categories(html):
    categories = [elem.text_content() for elem in html.xpath("//div[contains(@class,'event_body')]/p")]
    groupings = []
    for category_set in categories:
        grouping = category_set.split("Category:")[1].split(",")
        grouping = [elem.strip() for elem in grouping]
        grouping = [elem.replace("!","") for elem in grouping]
        groupings.append(",".join(grouping))
    return groupings


def scrape(num_pages_to_scrape):
    event_links = []
    dates = []
    event_titles = []
    categories = []
    for page in range(num_pages_to_scrape):
        iter_event_links, iter_dates, iter_event_titles, iter_categories = get_events_data(page)
        event_links += iter_event_links
        dates += iter_dates
        event_titles += iter_event_titles
        categories += iter_categories
    data = {
        "event_links":event_links,
        "dates":dates,
        "event_titles": event_titles,
        "categories": categories
    }
    df = pd.DataFrame(data)
    df.to_csv("parks_events_data.csv")


if __name__ == '__main__':
    scrape(50)
    
    
