import sqlite3
import requests
from unittest.mock import Mock
from pathlib import Path

import pytest
from scrapy.http import TextResponse, Request

from scripts.scripts_config import BASE_PATH

# --------------
# Helper Classes
# ---------------


class MockSuccessResponseFromStartPage(object):
    def __init__(self):
        self.text = self.html_response()
        self.raise_for_status = Mock()

    def html_response(self):
        return """
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
          <tr>
           <td>
             <a href="web/bibdigit/periodice/Magazine_3/">Magazine_3</a>
           </td>
          </tr>
        </table>
        """


class MockUnpearsableResponseFromStartPage(object):
    def __init__(self):
        self.text = self.html_response()
        self.raise_for_status = Mock()

    def html_response(self):
        return """
        <table>
          <tr>
           <td>
             <a href="web/bibdigit/test_periodice/Magazine_1/">Magazine_1</a>
           </td>
          </tr>
          <tr>
           <td>
             <a href="web/bibdigit/test_periodice/Magazine_2/">Magazine_2</a>
           </td>
          </tr>
        </table>
        """


class MockHTTPError(object):
    def __init__(self):
        self.exception = self.raise_exception()

    def raise_exception(self):
        raise requests.exceptions.HTTPError()


class MockConnectionError(object):
    def __init__(self):
        self.exception = self.raise_exception()

    def raise_exception(self):
        raise requests.exceptions.ConnectionError()


class MockTimeoutError(object):
    def __init__(self):
        self.exception = self.raise_exception()

    def raise_exception(self):
        raise requests.exceptions.Timeout()


class MockRequestException(object):
    def __init__(self):
        self.exception = self.raise_exception()

    def raise_exception(self):
        raise requests.exceptions.RequestException()


# ---------------
# Fixtures spider
# ---------------


@pytest.fixture
def get_html_response(file_name):

    url = "https://test_url.ro"

    request = Request(url=url)
    file_path = (
        Path(BASE_PATH) / "tests" / "test_spider" / "dummy_data_for_tests" / file_name
    )

    if ".html" in file_name:
        with open(file_path, "r") as f:
            file_content = f.read()
    elif ".pdf" in file_name:
        with open(file_path, "rb") as f:
            file_content = f.read()

    response = TextResponse(
        url=url, request=request, body=file_content, encoding="utf-8"
    )

    return response


# ----------------
# Fixtures scripts
# ----------------


@pytest.fixture
def mock_get_all_magazine_names_from_start_page_success_response(monkeypatch):

    def mock_get(url):
        return MockSuccessResponseFromStartPage()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_get_all_magazine_names_from_start_page_unparseable_response(monkeypatch):

    def mock_get(url):
        return MockUnpearsableResponseFromStartPage()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_HTTPError(monkeypatch):

    def mock_get_exception(url):
        return MockHTTPError()

    monkeypatch.setattr(requests, "get", mock_get_exception)


@pytest.fixture
def mock_ConnectionError(monkeypatch):

    def mock_get_exception(url):
        return MockConnectionError()

    monkeypatch.setattr(requests, "get", mock_get_exception)


@pytest.fixture
def mock_TimeoutError(monkeypatch):

    def mock_get_exception(url):
        return MockTimeoutError()

    monkeypatch.setattr(requests, "get", mock_get_exception)


@pytest.fixture
def mock_RequestException(monkeypatch):

    def mock_get_exception(url):
        return MockRequestException()

    monkeypatch.setattr(requests, "get", mock_get_exception)


@pytest.fixture
def get_all_magazine_names_from_start_page_warning_message():
    return "get_all_magazine_names_from_start_page() returns an empty list."


@pytest.fixture
def create_test_tb(tmp_path):
    path_db = tmp_path / "test.db"
    conn = sqlite3.connect(path_db)

    yield path_db


@pytest.fixture
def create_db_tables(create_test_tb):

    path_db = create_test_tb
    conn = sqlite3.connect(path_db)
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

    values_to_be_inserted = ["Magazine_2", "Magazine_5", "Magazine_6"]

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
def create_empty_test_file(tmp_path):

    target_file = tmp_path / "test_file.txt"

    with open(target_file, "x") as f:
        f.write("")

    return target_file


@pytest.fixture
def add_data_to_not_wanted_magazines_test_file(create_empty_test_file):

    target_file = create_empty_test_file

    data_to_be_written_in_file = ["Magazine_3", "Magazine_4"]

    with open(target_file, "a") as f:
        for data in data_to_be_written_in_file:
            f.write(data + "\n")

    return target_file, data_to_be_written_in_file
