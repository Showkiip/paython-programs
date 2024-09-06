# Scrapy settings for linkedin_scraper project

BOT_NAME = "linkedin_scraper"

SPIDER_MODULES = ["linkedin_scraper.spiders"]
NEWSPIDER_MODULE = "linkedin_scraper.spiders"

# Obey robots.txt rules (set to False if you are testing in an environment where it's acceptable)
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# This delay is important to prevent bans
DOWNLOAD_DELAY = 3

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # Uncomment if using Selenium
    # 'scrapy_selenium.SeleniumMiddleware': 800,
}

# Set up User-Agent rotation
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    # Add more user agents to mimic different browsers
]

# Proxy rotation to avoid IP bans
ROTATING_PROXY_LIST = [
    'http://proxy1.example.com:8000',
    'http://proxy2.example.com:8031',
    # Add more proxies or use a rotating proxy service
]

# Enable AutoThrottle to manage request rates dynamically
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5  # The initial download delay
AUTOTHROTTLE_MAX_DELAY = 60  # The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # The average number of requests Scrapy should be sending in parallel to each remote server
AUTOTHROTTLE_DEBUG = True  # Enable showing throttling stats for every response received

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Enable Retry middleware to handle request failures
RETRY_ENABLED = True
RETRY_TIMES = 5  # Number of times to retry a request in case of failure

# Enable cookies for authenticated sessions
COOKIES_ENABLED = True
