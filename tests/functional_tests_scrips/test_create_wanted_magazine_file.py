from scripts.create_wanted_magazines_file import main


def test_create_wanted_magazine_file_script(
    add_data_to_magazines_table,
    add_data_to_empty_test_file,
    tmp_path,
    mock_get_all_magazine_names_from_start_page_success_response,
):

    path_database, _ = add_data_to_magazines_table
    path_list_of_magazines_not_to_be_scrapped, _ = add_data_to_empty_test_file
    path_wanted_magazines = tmp_path / "wanted_magazines.txt"

    main(
        path_database, path_list_of_magazines_not_to_be_scrapped, path_wanted_magazines
    )

    assert path_wanted_magazines.is_file()

    with open(path_wanted_magazines) as f:
        res = f.read()
        res = res.split()
    assert res == ["Magazine_1"]
