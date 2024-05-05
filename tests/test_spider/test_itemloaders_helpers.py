import sqlite3

import pytest

from BcuSpider.itemsloaders_helpers import (
    remove_last_element_from_url,
    write_to_database,
    get_id_from_database,
    get_wanted_magazines_from_file,
)


class TestRemoveLastElementFromUrl:

    def test_remove_last_element_from_url(self):

        url = "https://www.name.com/A/B/C"
        expected_result = "https://www.name.com/A/B/"

        res = remove_last_element_from_url(url)

        assert res == expected_result


class TestWriteToDatabase:

    def test_write_to_database_in_magazines_table(self, create_db_tables):

        database_path = create_db_tables
        table = "magazines"
        values = ["Magazine_name", "Magazine_link"]
        data_from_db = []

        write_to_database(database_path, table, *values)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        with conn:
            inserted_magazine_name = c.execute("SELECT name from magazines").fetchone()[
                0
            ]
            data_from_db.append(inserted_magazine_name)

            inserted_magazine_link = c.execute(
                "SELECT magazine_link from magazines"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_link)

        assert data_from_db == values

    def test_write_to_database_in_magazine_year_table(self, create_db_tables):

        database_path = create_db_tables
        table = "magazine_year"
        values = [1, "Year", "Year_link"]
        data_from_db = []

        write_to_database(database_path, table, *values)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        with conn:
            inserted_magazine_id = c.execute(
                "SELECT magazine_id from magazine_year"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_id)

            inserted_magazine_year = c.execute(
                "SELECT year from magazine_year"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_year)

            inserted_magazine_year_link = c.execute(
                "SELECT magazine_year_link from magazine_year"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_year_link)

        assert data_from_db == values

    def test_write_to_database_in_magazine_number_table(self, create_db_tables):

        database_path = create_db_tables
        table = "magazine_number"
        values = [1, "Magazine_number", "Magazine_number_link"]
        data_from_db = []

        write_to_database(database_path, table, *values)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        with conn:
            inserted_magazine_year_id = c.execute(
                "SELECT magazine_year_id from magazine_number"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_year_id)

            inserted_magazine_number = c.execute(
                "SELECT magazine_number from magazine_number"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_number)

            inserted_magazine_number_link = c.execute(
                "SELECT magazine_number_link from magazine_number"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_number_link)

        assert data_from_db == values

    def test_write_to_database_in_magazine_number_content_table(self, create_db_tables):

        database_path = create_db_tables
        table = "magazine_number_content"
        values = [1, "Magazine_content", 2]
        data_from_db = []

        write_to_database(database_path, table, *values)

        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        with conn:
            inserted_magazine_number_id = c.execute(
                "SELECT magazine_number_id from magazine_number_content"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_number_id)

            inserted_magazine_content = c.execute(
                "SELECT magazine_content from magazine_number_content"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_content)

            inserted_magazine_page = c.execute(
                "SELECT magazine_page from magazine_number_content"
            ).fetchone()[0]
            data_from_db.append(inserted_magazine_page)

        assert data_from_db == values


class TestGetIdFromDatabase:

    def test_get_id_from_database_from_magazines_table(self, create_db_tables):

        database_path = create_db_tables
        values = ["Magazine_name", "Magazine_link"]

        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        with conn:
            c.execute(
                "INSERT INTO magazines(name, magazine_link) VALUES(?,?)",
                (values[0], values[1]),
            )

        res = get_id_from_database(database_path, "magazines", values[0])

        assert res == 1

    def test_get_id_from_database_from_magazine_year_table(self, create_db_tables):

        database_path = create_db_tables
        values = [1, "Year", "Year_link"]

        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        with conn:
            c.execute(
                "INSERT INTO magazine_year(magazine_id, year, magazine_year_link) VALUES (?, ?, ?)",
                (values[0], values[1], values[2]),
            )

        res = get_id_from_database(database_path, "magazine_year", *values[:2])

        assert res == 1

    def test_get_id_from_database_from_magazine_number_table(self, create_db_tables):

        database_path = create_db_tables
        values = [1, "Magazine_number", "Magazine_number_link"]

        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        with conn:
            c.execute(
                "INSERT INTO magazine_number(magazine_year_id, magazine_number, magazine_number_link) VALUES (?, ?, ?)",
                (values[0], values[1], values[2]),
            )

        res = get_id_from_database(database_path, "magazine_number", *values[:2])

        assert res == 1


class TestGetWantedMagazinesFromFile:

    def test_get_wanted_magazines_from_file_gets_data(
        self, add_data_to_empty_test_file
    ):

        file_path, file_data = add_data_to_empty_test_file
        res = get_wanted_magazines_from_file(file_path)

        assert res == file_data

    def test_get_wanted_magazines_from_file_missing_file(self, tmp_path, capsys):

        file_path = tmp_path / "file.txt"

        get_wanted_magazines_from_file(file_path)
        out, _ = capsys.readouterr()

        assert out.strip() == f"File not found at {file_path}"
