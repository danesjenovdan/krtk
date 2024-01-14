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
