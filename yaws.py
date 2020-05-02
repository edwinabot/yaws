import sqlite3
import os

import click


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


@click.group()
def main():
    pass


@click.command(name="new")
@click.option(
    "--crawl-path", "-p", required=True, help="Destination path for the crawl."
)
@click.option(
    "--domain",
    "-d",
    multiple=True,
    required=True,
    help="Domain to be crawled. Allows multiple.",
)
@click.option(
    "--max-requests", "-r", default=10, help="Maximum number of requests on each visit."
)
@click.option(
    "--max-concurrency",
    "-c",
    default=3,
    help="Maximum number of concurrent requests on each visit.",
)
@click.option("--crontab", "-t", default="*,*", help="Cron based schedule.")
def create_new_crawl(
    crawl_path, domain, max_requests, max_concurrency, crontab
) -> Settings:
    print("Creating a new crawl")
    settings = build_crawl_settings(
        crawl_path, domain, max_requests, max_concurrency, crontab
    )
    crawl_path = build_crawl_directory(settings.crawl_path)
    create_database(settings)
    return settings


@click.command(name="resume")
def resume_crawl(*args, **kwargs):
    pass


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
                "CREATE TABLE IF NOT EXISTS settings ("
                "          setting  TEXT PRIMARY KEY,"
                "          value    TEXT NOT NULL"
                ") WITHOUT ROWID"
            ),
            [],
        )
    except Exception as ex:
        print("Creating settings table: FAILED")
        print(ex)
        exit(1)
    else:
        print("Creating settings table: OK")

    # Create Visits table
    print("Creating visits table...")
    try:
        db.execute(
            (
                "CREATE TABLE IF NOT EXISTS visits ("
                "    url             TEXT PRIMARY KEY,"
                "    status_code     INTEGER,"
                "    last_visit      TEXT,"
                "    content         BLOB"
                ") WITHOUT ROWID"
            ),
            [],
        )
    except Exception as ex:
        print("Creating visits table: FAILED")
        print(ex)
        exit(1)
    else:
        print("Creating visits table: OK")

    # Insert settings

    print("Populating settings table...")
    try:
        setting_records = (
            ("crawl_path", settings.crawl_path),
            ("domains", ','.join(settings.domains)),
            ("requests", settings.requests),
            ("concurrency", settings.concurrency),
            ("schedule", settings.schedule),
        )
        db.executemany(
            "INSERT INTO settings (setting, value) VALUES (?, ?)", setting_records
        )
        db.commit()
    except Exception as ex:
        print("Populating visits table: FAILED")
        print(ex)
        exit(1)
    else:
        print("Populating visits table: OK")

    # Insert visits created from the target domains
    print("Populating visits table...")
    try:
        records = [(d,) for d in settings.domains]
        db.executemany("INSERT INTO visits (url) VALUES (?)", records)
        db.commit()
    except Exception as ex:
        print("Populating visits table: FAILED")
        print(ex)
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


if __name__ == "__main__":
    main.add_command(create_new_crawl)
    main.add_command(resume_crawl)
    main()
