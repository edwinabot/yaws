import sqlite3


def create_database(settings):
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
