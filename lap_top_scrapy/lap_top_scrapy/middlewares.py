# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

# для Middlewere selenium
from scrapy_selenium import SeleniumMiddleware
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TestScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TestScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RotatingProxyMiddleware:
    """
    Смена proxy после каждого запроса
    Заложена идея принудительной смены перед каждым запросом
    """

    def __init__(self, proxies, requests_per_proxy):
        self.proxies = proxies
        self.requests_per_proxy = requests_per_proxy
        self.proxy_index = 0
        self.request_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxies=crawler.settings.get("PROXY_LIST"),
            requests_per_proxy=crawler.settings.get("REQUESTS_PER_PROXY", 3),
        )

    def process_request(self, request, spider):
        if self.request_count >= self.requests_per_proxy:
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
            self.request_count = 0

        current_proxy = self.proxies[self.proxy_index]
        request.meta["proxy"] = current_proxy

        self.request_count += 1

        spider.logger.info(f"Using proxy: {current_proxy}")


class RandomUserAgentMiddleware:
    """
    Рандомная смена user-agent
    """

    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agents=crawler.settings.get("USER_AGENT_LIST"))

    def process_request(self, request, spider):
        # Выбираем случайный User-Agent для каждого запроса
        current_agent = random.choice(self.user_agents)
        request.headers["User-Agent"] = current_agent
        spider.logger.info(f"Using User-Agent: {current_agent}")


class CustomSeleniumMiddleware(SeleniumMiddleware):
    def __init__(
        self,
        driver_name,
        driver_executable_path=None,
        driver_arguments=None,
        *args,
        **kwargs,
    ):
        geckodriver_path = r"C:\DEV_python\PARSING\lap_top_scrapy\lap_top_scrapy\lap_top_scrapy\utils\geckodriver.exe"
        firefox_options = Options()
        firefox_options.headless = True
        
        service = Service(geckodriver_path)

        self.driver = Firefox(
            service=service, options=firefox_options
        )
