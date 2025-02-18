# Importing from old MySQL database

## Old database info

We're assuming you're coming from this type of database (used by [php-url-shortener](https://github.com/mathiasbynens/php-url-shortener)):

```
+-------+--------------+------+-----+---------+-------+
| Field | Type         | Null | Key | Default | Extra |
+-------+--------------+------+-----+---------+-------+
| slug  | varchar(14)  | NO   | PRI | NULL    |       |
| url   | varchar(620) | NO   |     | NULL    |       |
| date  | datetime     | NO   |     | NULL    |       |
| hits  | bigint(20)   | NO   |     | 0       |       |
+-------+--------------+------+-----+---------+-------+
```

## Creating a CSV export from the old database

You will need access to the old database directly on the machine where it is running since we will write out to a file directly

```sh
# connect to the `shortner` database
mysql -u djnd -p shortner

# this will write out a CSV file
SELECT * INTO OUTFILE '/tmp/dump.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' FROM redirect;
```

Example of `dump.csv` file:

```
"a","https://github.com/mathiasbynens/php-url-shortener","2014-05-13 14:18:41",17
"b","http://www.google.com","2014-05-13 14:57:45",11
```

Before importing old data make sure the new database is empty, since aliases are unique in the database and the import will fail if conflicting entries are present

```sh
# delete all entries
flask clear-db
```

You can now copy the created file to where krtk is installed and run the following command to import the data:

```sh
# import short links from csv dump
flask import-csv dump.csv
```

Congratulations, you imported all the old shortener links! 🎉

---
---
---

### Old instructions (manual import)

> [!NOTE]
> These are old instructions that are no longer up to date. Here only for information.

1. Hand-modify MySQL dump
    - Open `dump.sql`
    - Manually delete lines 1-39 in 55-67 (only INSERT statements should be left)
    - Search-replace `\'` with `''` (this is how quotes are escaped in SQLite)
    - Save `dump.sql`
2. Move into SQLite
    - Install [DB Browser for SQLite](https://sqlitebrowser.org/)
    - Open it and create a new DB called `data.db`
    - Go to the `Execute SQL` tab
    - Create a new table:
      ```sql
      CREATE TABLE "redirect" (
        "alias"	TEXT NOT NULL,
        "destination"	TEXT NOT NULL,
        "created"	DATETIME NOT NULL,
        "hits"	NUMERIC NOT NULL,
        PRIMARY KEY("alias"),
        UNIQUE("alias")
      )
      ```
    - `CTRL + SHIFT + T` to open `dump.sql` that was modified in 1. and execute it.
3. Modify to match new schema:
    ```sql
    ALTER TABLE redirect RENAME TO shortened_link;
    ALTER TABLE shortened_link DROP COLUMN hits;
    ALTER TABLE shortened_link ADD COLUMN is_custom BOOLEAN NOT NULL DEFAULT 0;
    PRAGMA writable_schema = 1;
    UPDATE SQLITE_MASTER SET SQL = 'CREATE TABLE "shortened_link" ("alias"	TEXT NOT NULL, "destination"	TEXT NOT NULL, "created"	DATETIME NOT NULL, "is_custom"	BOOLEAN NOT NULL,	PRIMARY KEY("alias"),	UNIQUE("alias"));' WHERE NAME = 'shortened_link';
    PRAGMA writable_schema = 0;
    ```
4. Add migration information:
    ```sql
    CREATE TABLE alembic_version (
      version_num VARCHAR(32) NOT NULL,
      CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
    );
    INSERT INTO alembic_version VALUES ('1a161105f005')
    ```
5. Save and move the `data.db` file to `instance` folder in `krtk` project
6. Run `flask db check` to confirm alembic is happy with the db state
