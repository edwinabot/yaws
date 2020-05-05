import os

from models import Settings


def build_crawl_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def build_crawl_settings(
    crawl_path, domains, requests, concurrency, schedule_expression
) -> Settings:
    settings = Settings(crawl_path, domains, requests, concurrency, schedule_expression)
    return settings
