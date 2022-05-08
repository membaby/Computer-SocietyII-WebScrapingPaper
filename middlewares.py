import selenium
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from .http import SeleniumRequest

class SeleniumMiddleware:
    def __init__(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def from_crawler(cls, crawler):
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if not isinstance(request, SeleniumRequest):
            return None
        self.browser.get(request.url)
        body = self.browser.page_source

        return HtmlResponse(
            self.browser.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        self.browser.quit()