from bs4 import BeautifulSoup
import bs4
import requests
import typing
from config import CONFIG


class Mipt:
    url: str = CONFIG["link"]["MIPT"]

    def last_news(self) -> bs4.element.Tag:
        resp = requests.get(self.url + "news/", headers=CONFIG['headers'])
        soup = BeautifulSoup(resp.text, "xml")
        last_news = soup.find("div", attrs={"class": "news-item"})
        return last_news

    def full_news(self) -> typing.List[str]:
        link = self.link()
        date = self.date()
        title = self.title()
        preview = self.preview()
        image = self.image()
        return [date, title, preview, link, image]

    def link(self) -> str:
        last_news = self.last_news()
        title_block = last_news.find("div", attrs={"class": "title-block"})
        title_link = title_block.find("a", attrs={"class": "title link"})
        link = self.url + title_link["href"]
        return link

    def date(self) -> str:
        last_news = self.last_news()
        title_block = last_news.find("div", attrs={"class": "title-block"})
        news_date = title_block.find("span", attrs={"class": "date"})
        return news_date.text.strip()

    def title(self) -> str:
        last_news = self.last_news()
        title_block = last_news.find("div", attrs={"class": "title-block"})
        title_link = title_block.find("a", attrs={"class": "title link"})
        return title_link.text.strip()

    def preview(self) -> str:
        last_news = self.last_news()
        content = last_news.find("div", attrs={"class": "contents"})
        news_text = content.find("div", attrs={"class": "summary"})
        return news_text.text.strip()

    def image(self) -> str:
        last_news = self.last_news()
        image_body = last_news.find("a", attrs={"class": "picture"})
        image = image_body.find("img")
        image_link = self.url + image["src"]
        return image_link
