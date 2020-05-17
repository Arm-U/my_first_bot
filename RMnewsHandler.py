from bs4 import BeautifulSoup
import bs4
import requests
import typing
from config import CONFIG


class RealMadrid:
    url: str = CONFIG["link"]["RM"]

    def last_news(self) -> bs4.element.Tag:
        resp = requests.get(self.url + "news/", headers=CONFIG['headers'])
        soup = BeautifulSoup(resp.text, "xml")
        last_news = soup.find("a", attrs={"class": "news-mini__link"})
        return last_news

    def full_news(self) -> typing.List[str]:
        link = self.link()
        date = self.date()
        title = self.title()
        preview = self.preview()
        return [date, title, preview, link]

    def link(self) -> str:
        last_news = self.last_news()
        link = self.url + last_news["href"]
        return link

    def date(self) -> str:
        last_news = self.last_news()
        news_body = last_news.find("div", attrs={"class": "news-mini__body"})
        news_mini_info = news_body.find("div", attrs={"class": "info news-mini__info"})
        news_date = news_mini_info.find("div", attrs={"class": "info__item info__item--date"})
        return news_date.text.strip()

    def title(self) -> str:
        last_news = self.last_news()
        news_body = last_news.find("div", attrs={"class": "news-mini__body"})
        news_title = news_body.find("h3")
        return news_title.text.strip()

    def preview(self) -> str:
        last_news = self.last_news()
        news_body = last_news.find("div", attrs={"class": "news-mini__body"})
        news_text_preview = news_body.find("div", attrs={"class": "news-mini__text-preview"})
        return news_text_preview.text.strip()
