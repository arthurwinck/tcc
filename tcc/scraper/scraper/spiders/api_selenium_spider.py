from dataclasses import asdict
import json
import time
from typing import Optional
from scrapy import Spider, Request  # type: ignore
from scrapy.http import Response  # type: ignore
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tcc.scraper.scraper.items import API2ParseDto, APIDocs
from tcc.scraper.scraper.utils import Utils


class APISeleniumSpider(Spider):
    name = "api_selenium_spider"

    def configure_spider(self):
        self.json_path = self.settings.get("JSON_FILE_PATH")

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(
            service=Service(self.settings.get("SELENIUM_DRIVER_EXECUTABLE_PATH")),
            options=chrome_options,
        )

    def start_requests(self):
        self.configure_spider()

        with open(self.json_path, "r") as f:
            raw_data = json.load(f)

        for item in raw_data:
            if item["docs"]["swagger_links"]:

                dto = API2ParseDto(
                    uuid=item["uuid"],
                    api_docs=APIDocs(
                        custom_links=item["docs"]["custom_links"],
                        swagger_links=item["docs"]["swagger_links"],
                    ),
                )

                url = dto.api_docs.swagger_links[0]
                yield Request(url, callback=self.parse, meta={"dto": dto})

    def parse(self, response: Response):
        self.driver.get(response.url)

        time.sleep(2.5)

        dto: API2ParseDto = response.meta["dto"]

        selector = Selector(text=self.driver.page_source)

        # Protótipo ainda só realiza a extração de dados para páginas swagger - primeira tentativa é a path para o link
        open_api_url: str | None = selector.css(".main a::attr(href)").get()

        # Segunda tentativa é o botão de download do json
        open_api_download_link: str | None = selector.css(
            ".api-info p a::attr(href)"
        ).get()

        if open_api_url:
            base_link = Utils.get_base_url(dto.api_docs.swagger_links[0])

            open_api_link = base_link + open_api_url

            yield {"uuid": dto.uuid, "open_api_link": open_api_link}

        elif open_api_download_link:

            yield {"uuid": dto.uuid, "open_api_link": open_api_download_link}

    def closed(self, reason):
        self.driver.quit()
