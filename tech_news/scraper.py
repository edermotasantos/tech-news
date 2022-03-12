import requests
import time
import parsel
import re


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


def summary_cleaner(summary):
    clean = re.compile("<.*?>")
    summary = re.sub(clean, '', summary)
    return summary


def convert_comments_count(comments_count):
    clean = re.compile("<.*?>")
    comments_count = re.sub(clean, '', comments_count)
    comments_count = int(comments_count[2:4])
    return comments_count


def name_writer_cleanner(writer, empty_space):
    if writer.endswith(empty_space):
        writer = writer[:-len(empty_space)]
    if writer.startswith(empty_space):
        writer = writer[1:]
    return writer


def sources_cleanner(sources, empty_space):
    sources_list = []
    for source in sources:
        if source.endswith(empty_space):
            source = source[:-len(empty_space)]
        if source.startswith(empty_space):
            source = source[1:]
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


# Requisito 4
def scrape_noticia(html_content):
    dict = {}
    empty_space = " "
    selector = parsel.Selector(text=fetch(html_content))

    title_and_date_container = ".z--pt-40.z--pb-24.z--pl-16"
    share_comments_and_author_container = "#js-author-bar.tec--author"

    title = selector.css(title_and_date_container + " h1::text").get()
    timestamp = selector.css(
        title_and_date_container + " time::attr(datetime)"
        ).get()
    writer = selector.css(
        share_comments_and_author_container + " a.tec--link--tecmundo::text"
        ).get()
    shares_count = selector.css(
        share_comments_and_author_container + " .tec--toolbar__item::text"
        ).get()
    comments_count = selector.css(
        share_comments_and_author_container + " div button"
        ).get()
    summary = selector.css(
        ".tec--article__body-grid .tec--article__body.z--px-16.p402_premium p"
        ).get()
    sources = selector.css(".z--mb-16.z--px-16 div a::text").getall()
    categories = selector.css(
        ".z--px-16 div#js-categories a::text"
        ).getall()

    if shares_count is None:
        shares_count = 0
    else:
        shares_count = convert_shares_count(shares_count)
    summary = summary_cleaner(summary)
    comments_count = convert_comments_count(comments_count)
    writer = name_writer_cleanner(writer, empty_space)
    sources_list = sources_cleanner(sources, empty_space)
    categories_list = categories_cleanner(categories, empty_space)

    dict["url"] = html_content
    dict["title"] = title
    dict["timestamp"] = timestamp
    dict["writer"] = writer
    dict["shares_count"] = shares_count
    dict["comments_count"] = comments_count
    dict["summary"] = summary
    dict["sources"] = sources_list
    dict["categories"] = categories_list

    return dict


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
