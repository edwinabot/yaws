class Settings:
    def __init__(self, crawl_path, domains, requests, concurrency, schedule):
        self.crawl_path = crawl_path
        self.domains = domains
        self.requests = requests
        self.concurrency = concurrency
        self.schedule = schedule


class Visit:
    def __init__(self, url, datetime, status_code):
        self.url = url
        self.datetime = datetime
        self.status_code = status_code
