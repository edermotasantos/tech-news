import re
import datetime
from tech_news.database import (
    search_news,
)


# Requisito 6
def search_by_title(title):
    list = []
    # re.compile(title, re.IGNORECASE) para "case insensitive"
    titles_news = search_news({"title": re.compile(title, re.IGNORECASE)})
    for title_news in titles_news:
        list.append((title_news["title"], title_news["url"]))
    return list


# Requisito 7
def search_by_date(date):
    date_format = "%Y-%m-%d"
    list = []
    try:
        is_valid_date = datetime.datetime.strptime(date, date_format)
        if is_valid_date:
            dates_news = search_news(
                {
                    "timestamp": re.compile(date, re.IGNORECASE)
                }
            )
            for date_news in dates_news:
                list.append((date_news["title"], date_news["url"]))
            return list
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    list = []
    sources_news = search_news({"sources": re.compile(source, re.IGNORECASE)})
    for source_news in sources_news:
        list.append((source_news["title"], source_news["url"]))
    return list


# Requisito 9
def search_by_category(category):
    list = []
    categories_news = search_news(
        {
            "categories": re.compile(category, re.IGNORECASE)
        }
    )
    for category_news in categories_news:
        list.append((category_news["title"], category_news["url"]))
    return list
