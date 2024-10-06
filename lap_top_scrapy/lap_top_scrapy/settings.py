from shutil import which
from datetime import datetime
from pathlib import Path
# Scrapy settings for lap_top_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

PROJECT_ROOT = Path(__file__).resolve().parent

BOT_NAME = "lap_top_scrapy"

SPIDER_MODULES = ["lap_top_scrapy.spiders"]
NEWSPIDER_MODULE = "lap_top_scrapy.spiders"


LOG_LEVEL = (
    "INFO"  # если поставить DEBUG то в логи прилетает весь контент и Scrapy вылетает
)
LOG_FILE = (
    f"lap_top_scrapy\\logs\\log_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log"
)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "lap_top_scrapy (+http://www.yourdomain.com)"

# Obey robots.txt rules  Если поставить True то Scrapy лезет в robot.txt и потом вылетает
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "lap_top_scrapy.middlewares.LapTopScrapySpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "lap_top_scrapy.middlewares.LapTopScrapyDownloaderMiddleware": 543,
    "lap_top_scrapy.middlewares.RandomUserAgentMiddleware": 400,
    "lap_top_scrapy.middlewares.RotatingProxyMiddleware": 543,
    "lap_top_scrapy.middlewares.CustomSeleniumMiddleware": 800,
}

USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    # Добавьте больше User-Agent строк
] 

PROXY_LIST = [
    'https://nndtcT:nn95fDCcfX@46.8.15.241:1050',
    'https://MSEbx5:zC0YMc@147.45.52.226:9024',
    'https://nndtcT:nn95fDCcfX@46.8.23.171:1050',
    'https://nndtcT:nn95fDCcfX@31.40.203.43:1050',
    'https://nndtcT:nn95fDCcfX@109.248.205.109:1050',
    'https://nndtcT:nn95fDCcfX@188.130.186.172:1050',
    # Добавьте сюда больше прокси
]

REQUEST_PER_PROXY = 2

SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS = ['--headless']

GECKODRIVER_PATH = PROJECT_ROOT / "utils" / "geckodriver.exe"

CONFIGFILE_PATH = PROJECT_ROOT / "utils" / "config.xlsx"

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "lap_top_scrapy.pipelines.LapTopScrapyPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
