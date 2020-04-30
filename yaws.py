import sqlite3
import os


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


def main():
    new_crawl = True
    matches = None
    if new_crawl:
        settings = create_new_crawl(matches)
        start_crawl(settings)


def create_new_crawl(matches) -> Settings:
    print("Creating a new crawl")

    domains = []
    crawl_path = ""
    requests = 1
    concurrency = 1
    schedule = "*,*"

    crawl_path = build_crawl_directory(matches.path)
    domains.extend(matches.domains)
    settings = build_crawl_settings(
        crawl_path, domains, requests, concurrency, schedule
    )

    create_database(settings)

    return settings


def create_database(settings: Settings):
    db_path = settings.crawl_path + "/db.sqlite"
    print("Creating database...")
    db = sqlite3.connect(db_path)
    print("Creating database: OK")

    # Create and populate Settings table
    print("Creating settings table...")
    try:
        db.execute(
            (
                "CREATE TABLE IF NOT EXISTS settings (",
                "          setting  TEXT PRIMARY KEY,",
                "          value    TEXT NOT NULL",
                ") WITHOUT ROWID",
            ),
            [],
        )
    except:
        print("Creating settings table: FAILED")
        exit(1)
    else:
        print("Creating settings table: OK")

    # Create Visits table
    print("Creating visits table...")
    try:
        db.execute(
            '"CREATE TABLE IF NOT EXISTS visits (',
            "    url             TEXT PRIMARY KEY,",
            "    status_code     INTEGER,",
            "    last_visit      TEXT,",
            "    content         BLOB",
            ') WITHOUT ROWID"',
            [],
        )
    except:
        print("Creating visits table: FAILED")
        exit(1)
    else:
        print("Creating visits table: OK")

    # Insert settings

    print("Populating settings table...")

    print("Populating settings table: OK")

    # Insert visits created from the target domains
    print("Populating visits table...")
    try:
        db.executemany("INSERT INTO visits (url) VALUES (?)", settings.domains)
    except:
        print("Populating visits table: FAILED")
        exit(1)
    else:
        print("Populating visits table: OK")


def start_crawl(settings: Settings):
    print("The crawl should have started by now...")


def build_crawl_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def build_crawl_settings(
    crawl_path, domains, requests, concurrency, schedule_expression
) -> Settings:
    settings = Settings(crawl_path, domains, requests, concurrency, schedule_expression)
    return settings
