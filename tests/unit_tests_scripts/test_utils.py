from scripts.utils import (
    get_already_inserted_magazine_name,
    get_not_wanted_magazines,
    get_all_magazine_names_from_start_page,
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
        self, capsys, create_test_tb
    ):

        path_db = create_test_tb

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
        self, capsys, create_not_wanted_magazines_test_file
    ):

        file_path = create_not_wanted_magazines_test_file

        res = get_not_wanted_magazines(file_path)
        out, _ = capsys.readouterr()

        assert (
            "The 'list_of_magazines_not_to_be_scrapped.txt' does not exists at"
            f" {file_path}" not in out
        )

        assert (
            "get_not_wanted_magazines() returns an empty list."
            f" Check {file_path}"
            " file if it is empty." in out
        )

        assert res == []

    def test_get_not_wanted_magazines_with_data_in_file(
        self, add_data_to_not_wanted_magazines_test_file
    ):

        file_path, file_values = add_data_to_not_wanted_magazines_test_file

        res = get_not_wanted_magazines(file_path)

        assert res == file_values


class TestGetAllMagazineNamesFromStartPage:

    def test_get_all_magazine_names_from_start_page_success(
        self, mock_get_all_magazine_names_from_start_page_success_response
    ):
        regular_expression = MAGAZINE_LINKS_REGEX
        res = get_all_magazine_names_from_start_page("url", regular_expression)

        assert res == ["Magazine_1", "Magazine_2"]

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
