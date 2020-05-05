import click

import database as db
import crawls as cr


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
def create_new_crawl(crawl_path, domain, max_requests, max_concurrency, crontab):
    print("Creating a new crawl")
    settings = cr.build_crawl_settings(
        crawl_path, domain, max_requests, max_concurrency, crontab
    )
    crawl_path = cr.build_crawl_directory(settings.crawl_path)
    db.create_database(settings)
    return settings


@click.command(name="resume")
def resume_crawl(*args, **kwargs):
    pass


def start_crawl(settings):
    print("The crawl should have started by now...")


if __name__ == "__main__":
    main.add_command(create_new_crawl)
    main.add_command(resume_crawl)
    main()
