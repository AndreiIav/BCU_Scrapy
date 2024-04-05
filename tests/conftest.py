import pytest
import sqlite3


@pytest.fixture
def create_test_tb(tmp_path):
    path_db = tmp_path / "test.db"
    conn = sqlite3.connect(path_db)

    yield path_db


@pytest.fixture
def create_db_tables(create_test_tb):

    path_db = create_test_tb
    conn = sqlite3.connect(path_db)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

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

    yield path_db


@pytest.fixture
def add_data_to_magazines_table(create_db_tables):

    path_db = create_db_tables

    conn = sqlite3.connect(path_db)
    c = conn.cursor()

    values_to_be_inserted = ["Magazine_1", "Magazine_2", "Magazine_3"]

    with conn:
        for value in values_to_be_inserted:
            c.execute(
                f"""
                INSERT INTO magazines(name)
                Values ('{value}')
                """
            )

    yield path_db, values_to_be_inserted
