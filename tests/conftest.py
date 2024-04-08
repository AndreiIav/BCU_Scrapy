import pytest
import sqlite3
import requests

# Helper Classes


class MockSuccessResponseFromStartPage(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.text = self.html_response()

    def html_response(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>

        <table>
          <tr>
           <td>
             <a href="web/bibdigit/periodice/Magazine_1/">Magazine_1</a>
           </td>
          </tr>
          <tr>
           <td>
             <a href="web/bibdigit/periodice/Magazine_2/">Magazine_2</a>
           </td>
          </tr>
        </table>
        
        </body>
        </html> 
        """


# Fixtures


@pytest.fixture
def mock_get_all_magazine_names_from_start_page_success_response(monkeypatch):

    def mock_get(url):
        return MockSuccessResponseFromStartPage(url)

    url = "start_url"
    monkeypatch.setattr(requests, "get", mock_get)


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


@pytest.fixture
def create_not_wanted_magazines_test_file(tmp_path):

    target_file = tmp_path / "test_file.txt"

    with open(target_file, "x") as f:
        f.write("")

    return target_file


@pytest.fixture
def add_data_to_not_wanted_magazines_test_file(create_not_wanted_magazines_test_file):

    target_file = create_not_wanted_magazines_test_file

    data_to_be_written_in_file = ["Magazine_4", "Magazine_5"]

    with open(target_file, "a") as f:
        for data in data_to_be_written_in_file:
            f.write(data + "\n")

    return target_file, data_to_be_written_in_file
