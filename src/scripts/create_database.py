import sqlite3
from pathlib import Path

from scripts_config import BASE_PATH, DATABASE_NAME

path_database = Path(BASE_PATH) / DATABASE_NAME

conn = sqlite3.connect(path_database)
conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
c = conn.cursor()

# Create database and tables.
with conn:
    c.executescript(
        """
        CREATE TABLE magazines(
        id integer PRIMARY KEY ,
        name text,
        magazine_link text);

        CREATE TABLE magazine_year(
        id integer PRIMARY KEY,
        magazine_id integer,
        year text,
        magazine_year_link text,
        FOREIGN KEY(magazine_id) REFERENCES magazines(id));

        CREATE TABLE magazine_number(
        id integer PRIMARY KEY,
        magazine_year_id integer,
        magazine_number text,
        magazine_number_link text,
        FOREIGN KEY(magazine_year_id) REFERENCES magazine_year(id));

        CREATE TABLE magazine_number_content(
        id integer PRIMARY KEY,
        magazine_number_id integer,
        magazine_content text,
        magazine_page id,
        FOREIGN KEY(magazine_number_id) REFERENCES magazine_number(id));
        """
    )

conn.close()
