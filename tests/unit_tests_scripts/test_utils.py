import pytest
import sqlite3

# from pathlib import Path

from scripts.utils import get_already_inserted_magazine_name


class TestGetAlreadyInsertedMagazineName:
    def test_get_already_inserted_magazine_name_with_no_existing_database(
        self, tmp_path, capsys
    ):

        get_already_inserted_magazine_name(tmp_path)
        out, _ = capsys.readouterr()

        assert (
            "sqlite3.OperationalError: unable to open database file' error "
            f"raised because there is no database at {tmp_path}" in out
        )

    def test_get_already_inserted_magazine_name_with_no_existing_magazines_table(
        self, tmp_path, capsys
    ):

        path_db = tmp_path / "test.db"
        conn = sqlite3.connect(path_db)

        get_already_inserted_magazine_name(path_db)
        out, _ = capsys.readouterr()

        assert (
            "'sqlite3.OperationalError: no such table: magazines' error raised"
            " in get_already_inserted_magazine_name()." in out
        )
