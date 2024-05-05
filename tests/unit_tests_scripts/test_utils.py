import pytest

from scripts.utils import (
    get_already_inserted_magazine_name,
    get_not_wanted_magazines,
    get_all_magazine_names_from_start_page,
    write_wanted_magazines_file,
)
from scripts.scripts_config import MAGAZINE_LINKS_REGEX


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
        self, capsys, create_test_db
    ):

        path_db = create_test_db

        get_already_inserted_magazine_name(path_db)
        out, _ = capsys.readouterr()

        assert (
            "'sqlite3.OperationalError: no such table: magazines' error raised"
            " in get_already_inserted_magazine_name()." in out
        )

    def test_get_already_inserted_magazine_name_with_empty_magazines_table(
        self, capsys, create_db_tables
    ):

        path_db = create_db_tables

        already_inserted_magazines = get_already_inserted_magazine_name(path_db)
        out, _ = capsys.readouterr()

        assert already_inserted_magazines == []
        assert (
            "get_already_inserted_magazine_name() returns an empty list."
            f" Check magazines table in {path_db}." in out
        )

    def test_get_already_inserted_magazine_name_with_non_empty_response(
        self, add_data_to_magazines_table
    ):

        path_db, inserted_values = add_data_to_magazines_table

        already_inserted_magazines = get_already_inserted_magazine_name(path_db)

        assert len(already_inserted_magazines) == len(inserted_values)
        assert already_inserted_magazines == inserted_values


class TestGetNotWantedMagazines:

    def test_get_not_wanted_magazines_file_does_not_exists(self, tmp_path, capsys):

        file_path = tmp_path / "file.txt"

        res = get_not_wanted_magazines(file_path)
        out, _ = capsys.readouterr()

        assert (
            "The 'list_of_magazines_not_to_be_scrapped.txt' does not exists at"
            f" {file_path}" in out
        )
        assert res == []

    def test_get_not_wanted_magazines_with_empty_file(
        self, capsys, create_empty_test_file
    ):

        file_path = create_empty_test_file

        res = get_not_wanted_magazines(file_path)
        out, _ = capsys.readouterr()

        assert (
            "get_not_wanted_magazines() returns an empty list."
            f" Check {file_path}"
            " file if it is empty." in out
        )

        assert res == []

    def test_get_not_wanted_magazines_with_data_in_file(
        self, add_data_to_empty_test_file
    ):

        file_path, file_values = add_data_to_empty_test_file

        res = get_not_wanted_magazines(file_path)

        assert res == file_values


class TestGetAllMagazineNamesFromStartPage:

    def test_get_all_magazine_names_from_start_page_success(
        self, mock_get_all_magazine_names_from_start_page_success_response
    ):
        regular_expression = MAGAZINE_LINKS_REGEX
        res = get_all_magazine_names_from_start_page("url", regular_expression)

        assert res == ["Magazine_1", "Magazine_2", "Magazine_3"]

    def test_get_all_magazine_names_from_start_page_unparseable_response(
        self,
        mock_get_all_magazine_names_from_start_page_unparseable_response,
        get_all_magazine_names_from_start_page_warning_message,
        capsys,
    ):

        warning_message = get_all_magazine_names_from_start_page_warning_message
        regular_expression = MAGAZINE_LINKS_REGEX
        url = "start_url"
        get_all_magazine_names_from_start_page(url, regular_expression)

        out, _ = capsys.readouterr()

        assert f"the response from {url} could not be parsed." in out
        assert warning_message in out

    def test_get_all_magazine_names_from_start_page_HTTPError(
        self,
        mock_HTTPError,
        get_all_magazine_names_from_start_page_warning_message,
        capsys,
    ):

        warning_message = get_all_magazine_names_from_start_page_warning_message
        url = "start_url"
        get_all_magazine_names_from_start_page(url, "regular_expression")

        out, _ = capsys.readouterr()

        assert f"{url} cannot be reached due to a HTTP Error." in out
        assert warning_message in out

    def test_get_all_magazine_names_from_start_page_ConnectionError(
        self,
        mock_ConnectionError,
        get_all_magazine_names_from_start_page_warning_message,
        capsys,
    ):

        warning_message = get_all_magazine_names_from_start_page_warning_message
        url = "start_url"
        get_all_magazine_names_from_start_page(url, "regular_expression")

        out, _ = capsys.readouterr()

        assert f"{url} cannot be reached due to a Connection Error." in out
        assert warning_message in out

    def test_get_all_magazine_names_from_start_page_TimeoutError(
        self,
        mock_TimeoutError,
        get_all_magazine_names_from_start_page_warning_message,
        capsys,
    ):

        warning_message = get_all_magazine_names_from_start_page_warning_message
        url = "start_url"
        get_all_magazine_names_from_start_page(url, "regular_expression")

        out, _ = capsys.readouterr()

        assert f"{url} cannot be reached due to a Timeout Error." in out
        assert warning_message in out

    def test_get_all_magazine_names_from_start_page_RequestException(
        self,
        mock_RequestException,
        get_all_magazine_names_from_start_page_warning_message,
        capsys,
    ):

        warning_message = get_all_magazine_names_from_start_page_warning_message
        url = "start_url"
        get_all_magazine_names_from_start_page(url, "regular_expression")

        out, _ = capsys.readouterr()

        assert f"{url} cannot be reached due to a Request Exception." in out
        assert warning_message in out


class TestWriteWantedMagazinesFile:

    def test_write_wanted_magazines_file_already_exists(
        self, capsys, create_empty_test_file
    ):

        path_wanted_magazines = create_empty_test_file

        write_wanted_magazines_file("", "", "", path_wanted_magazines)
        out, _ = capsys.readouterr()

        assert (
            f"{path_wanted_magazines} already exists. Remove it before attempting"
            " to create a new one." in out
        )

    def test_write_wanted_magazines_file_not_created(self, capsys, tmp_path):

        all_magazine_names_from_start_page = ["Magazine_1"]
        already_inserted_magazine_name = ["Magazine_1"]
        not_wanted_magazines = []
        path_wanted_magazines = tmp_path / "test_file.txt"

        write_wanted_magazines_file(
            all_magazine_names_from_start_page,
            already_inserted_magazine_name,
            not_wanted_magazines,
            path_wanted_magazines,
        )
        out, _ = capsys.readouterr()

        assert (
            f"{path_wanted_magazines} file was not created because there was"
            " no magazine name to be written in the file." in out
        )

    def test_write_wanted_magazines_file_is_created(self, capsys, tmp_path):

        all_magazine_names_from_start_page = ["Magazine_1"]
        already_inserted_magazine_name = []
        not_wanted_magazines = []
        path_wanted_magazines = tmp_path / "test_file.txt"

        write_wanted_magazines_file(
            all_magazine_names_from_start_page,
            already_inserted_magazine_name,
            not_wanted_magazines,
            path_wanted_magazines,
        )
        out, _ = capsys.readouterr()

        assert (
            f"wanted_magazines.txt file was created at {path_wanted_magazines}" in out
        )

    test_values = [
        (["a", "b", "c"], [], [], ["a", "b", "c"]),
        (["a", "b", "c"], ["a"], [], ["b", "c"]),
        (["a", "b", "c"], [], ["b"], ["a", "c"]),
        (["a", "b", "c"], ["d"], ["e"], ["a", "b", "c"]),
        (["a", "b", "c", "d"], ["a"], ["b", "c"], ["d"]),
    ]

    @pytest.mark.parametrize(
        "all_magazines,already_inserted,not_wanted,expected", test_values
    )
    def test_write_wanted_magazines_file_is_correct(
        self, tmp_path, all_magazines, already_inserted, not_wanted, expected
    ):
        path_wanted_magazines = tmp_path / "test_file.txt"

        write_wanted_magazines_file(
            all_magazines,
            already_inserted,
            not_wanted,
            path_wanted_magazines,
        )
        with open(path_wanted_magazines) as f:
            content = f.read()
            file_content = content.split()

        assert file_content == expected
