from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
import web2vec as w2v


class Web2VecCrawler:
    def __init__(self):
        self.items = []

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def crawl(self):
        process = CrawlerProcess(
            settings={
                "DEPTH_LIMIT": 1,
                "LOG_LEVEL": "INFO",
            }
        )

        dispatcher.connect(self.item_scraped, signal=signals.item_scraped)

        process.crawl(
            w2v.Web2VecSpider,
            start_urls=["https://sebastian.dancau.net"],  # pages to process
            allowed_domains=["dancau.net"],  # domains to process for links
            extractors=[
                w2v.HtmlBodyExtractor()
            ],  # extractors to use
        )
        process.start()
        return self.items


if __name__ == "__main__":
    crawler = Web2VecCrawler()
    result = crawler.crawl()
    print(result)