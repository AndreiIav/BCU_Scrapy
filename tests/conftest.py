import sqlite3
import requests
from unittest.mock import Mock

import pytest

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


# --------
# Fixtures
# --------


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
        c.execute(
            """
            CREATE TABLE magazines(
            id integer PRIMARY KEY ,
            name text,
            magazine_link text);
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
