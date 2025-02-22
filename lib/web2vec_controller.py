from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
import web2vec as w2v
import tldextract


class Web2VecController:
    def __init__(self):
        self.items = []
        self.extractors_map = {
            "dns": w2v.DNSExtractor,
            "html": w2v.HtmlBodyExtractor,
            "http": w2v.HttpResponseExtractor,
            "certificate": w2v.CertificateExtractor,
            "url_geo": w2v.UrlGeoExtractor,
            "url_lexical": w2v.UrlLexicalExtractor,
            "whois": w2v.WhoisExtractor,
            "google_index": w2v.GoogleIndexExtractor,
            "open_page_rank": w2v.OpenPageRankExtractor,
            "similar_web": w2v.SimilarWebExtractor,
            "url_haus": w2v.UrlHausExtractor
        }

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def crawl(self, start_url, extractors=None, allowed_domains=None, depth_limit=1):
        process = CrawlerProcess(
            settings={
                "DEPTH_LIMIT": depth_limit,
                "LOG_LEVEL": "INFO",
            }
        )

        if allowed_domains is None:
            # extract domain from start_url
            extracted = tldextract.extract(start_url)
            allowed_domains = [f'{extracted.domain}.{extracted.suffix}']

        if extractors is None:
            extractors = [w2v.HtmlBodyExtractor()]
        else:
            extractors = [self.extractors_map[extractor]() for extractor in extractors]

        dispatcher.connect(self.item_scraped, signal=signals.item_scraped)

        process.crawl(
            w2v.Web2VecSpider,
            start_urls=[start_url],  # pages to process
            allowed_domains=allowed_domains,  # domains to process for links
            extractors=extractors,  # extractors to use
        )
        process.start()
        return self.items
