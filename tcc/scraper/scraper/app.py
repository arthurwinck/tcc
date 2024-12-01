from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from tcc.scraper.scraper.spiders.api_selenium_spider import APISeleniumSpider
from tcc.scraper.scraper.spiders.conecta_api_spider import ConectaApiSpider


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ConectaApiSpider)
    yield runner.crawl(APISeleniumSpider)
    reactor.stop()  # type: ignore


if __name__ == "__main__":
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    crawl()
    reactor.run()  # type: ignore
