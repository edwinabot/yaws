# yaws
Yet another web scrapper

## Usage

### New crawl

When starting a crawl (using `--new` and providing the `--domains`) creates a directory and within it a persistance file that will record:

* url
* relative path to raw content
* date of visit

```bash
$ yaws --new --crawl-path /path/to/storage --domains foo.com,bar.com,baz.com
```

To immediataly start crawling add the `--start`

### Resume crawl

It is possible to resume a crawl (using `--resume` and `--crawl-path`)

```bash
$ yaws --resume --crawl-path /path/to/crawl
```

### Setting concurrency, requests and schedule

`--concurrency` argument adds a maximum number of concurrent requests to be performed on a domain. The `--schedule` parameter
sets visits using [crontab syntax](https://crontab.guru/#*/5_4-6_*_*_*) (only minutes and hours). The `--requests` parameter
total number of petitions per visit. This arguments can be set on new and resume crawls.

```bash
$ yaws --resume --crawl-path /path/to/crawl --requests 100 --concurrency 10 --schedule */5,4-6
```

This call will resume a crawl and will visit a domain at every 5th minute past every hour from 4 through 6.
It will perform 100 requests per visit limiting its concurrency to 10.
