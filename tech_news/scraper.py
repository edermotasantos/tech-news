import requests
import time
import parsel
import re
from tech_news.database import (
    create_news,
)


def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        time.sleep(1)
    except requests.ReadTimeout:
        return None
    except requests.HTTPError:
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = parsel.Selector(html_content)
    css_classes_prefix = ".tec--list.tec--list--lg"
    css_classes_suffix = " a.tec--card__thumb__link::attr(href)"
    url_list = selector.css(
        css_classes_prefix + css_classes_suffix
        ).getall()
    return url_list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)
    div = ".tec--list.tec--list--lg"
    url_next_class_prefix = " a.tec--btn.tec--btn--lg.tec--btn--primary"
    css_class_suffix = ".z--mx-auto.z--mt-48::attr(href)"
    next_page = selector.css(
        div + url_next_class_prefix + css_class_suffix
        ).get()
    return next_page


def convert_shares_count(shares_count):
    if shares_count[0] == " ":
        shares_count = int(shares_count[1:3])
    return shares_count


def convert_comments_count(comments_count):
    clean = re.compile("<.*?>")
    comments_count = re.sub(clean, '', comments_count)
    comments_count = int(comments_count[2:4])
    return comments_count


def name_writer_cleanner(writer, empty_space):
    if writer.endswith(empty_space):
        writer = writer[1:-len(empty_space)]
    return writer


def sources_cleanner(sources, empty_space):
    sources_list = []
    for source in sources:
        if source.endswith(empty_space):
            source = source[1:-len(empty_space)]
            sources_list.append(source)
    return sources_list


def categories_cleanner(categories, empty_space):
    categories_list = []
    for category in categories:
        if category.endswith(empty_space):
            category = category[:-len(empty_space)]
        if category.startswith(empty_space):
            category = category[1:]
            categories_list.append(category)
    return categories_list


def new_search_title(title, selector):
    if title is None:
        title = selector.css(
            ".z--pt-40.z--pb-24" + " h1::text"
        ).get()
    return title


def new_search_timestamp(timestamp, selector):
    if timestamp is None:
        timestamp = selector.css(
            ".z--pt-40.z--pb-24" + " time::attr(datetime)"
        ).get()
    return timestamp


def new_search_writer(selector):
    writer = selector.css(
        ".z--pt-40.z--pb-24" + " a::text"
    ).get()
    if writer is None:
        writer = selector.css(
            "#js-author-bar.tec--author p a::text"
        ).get()
    if writer is None:
        writer = selector.css(
            ".z--m-none. > a"
        ).get()
    return writer


def new_search_comments(comments_count, selector):
    if comments_count is None:
        comments_count = selector.css(
            ".z--pt-40.z--pb-24" + " button"
        ).get()
    return comments_count


def check_name_writer(writer):
    if writer == "@tec_mundo":
        writer = 'Equipe TecMundo'
    return writer


# Requisito 4
def scrape_noticia(html_content):
    dict = {}
    empty_space = " "

    selector = parsel.Selector(html_content)

    news_url = selector.xpath("/html/head/link[@rel='canonical']/@href").get()

    title_and_date_container = ".z--pt-40.z--pb-24.z--pl-16"

    share_comments_and_author_container = "#js-author-bar.tec--author"

    title = selector.css(
        title_and_date_container + " h1::text"
        ).get()

    title = new_search_title(title, selector)

    timestamp = selector.css(
        title_and_date_container + " time::attr(datetime)"
        ).get()

    timestamp = new_search_timestamp(timestamp, selector)

    writer = new_search_writer(selector)

    shares_count = selector.css(
        share_comments_and_author_container + " .tec--toolbar__item::text"
        ).get()
    comments_count = selector.css(
        share_comments_and_author_container + " div button"
        ).get()

    comments_count = new_search_comments(comments_count, selector)

    summary = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
        ).getall()

    summary = "".join(summary)

    sources = selector.css(".z--mb-16.z--px-16 div a::text").getall()

    categories = selector.css(
        "#js-categories *::text"
    ).getall()

    if len(sources) == 0:
        sources = selector.css(
         ".z--mb-16 div >::text"
        ).getall()

    if shares_count is None:
        shares_count = 0
    else:
        shares_count = convert_shares_count(shares_count)

    if comments_count is None:
        comments_count = 0
    else:
        comments_count = convert_comments_count(comments_count)

    writer = name_writer_cleanner(writer, empty_space)
    sources_list = sources_cleanner(sources, empty_space)
    categories_list = categories_cleanner(categories, empty_space)

    writer = check_name_writer(writer)

    dict["url"] = news_url
    dict["title"] = title
    dict["timestamp"] = timestamp
    dict["writer"] = writer
    dict["shares_count"] = shares_count
    dict["comments_count"] = comments_count
    dict["summary"] = summary
    dict["sources"] = sources_list
    dict["categories"] = categories_list

    return dict


def move_to_the_next_page(amount, html_content, scrape_news_list):
    while amount > 0:
        amount = amount - 20
        if amount <= 0:
            break
        url = scrape_next_page_link(html_content)
        html_content = fetch(url)
        scrape_page_next_page = scrape_novidades(html_content)[:amount]
        scrape_news_list.extend(scrape_page_next_page)
    return scrape_news_list


# Requisito 5
def get_tech_news(amount):
    list_dict_news = []
    url = "https://www.tecmundo.com.br/novidades"
    html_content = fetch(url)

    scrape_news_list = scrape_novidades(html_content)[:amount]

    move_to_the_next_page(amount, html_content, scrape_news_list)

    for url_item in range(len(scrape_news_list)):
        html_content = fetch(scrape_news_list[url_item])
        scrap_news = scrape_noticia(html_content)
        list_dict_news.append(scrap_news)

    create_news(list_dict_news)

    return list_dict_news
