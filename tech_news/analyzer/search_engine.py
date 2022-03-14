import re
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
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
