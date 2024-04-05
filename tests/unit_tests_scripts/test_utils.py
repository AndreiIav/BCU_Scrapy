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
