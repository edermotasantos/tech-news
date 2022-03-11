import requests
import time
import parsel


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


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
