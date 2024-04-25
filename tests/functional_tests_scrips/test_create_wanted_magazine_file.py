from scripts.utils import (
    get_already_inserted_magazine_name,
    get_not_wanted_magazines,
    get_all_magazine_names_from_start_page,
    write_wanted_magazines_file,
)
from scripts.scripts_config import MAGAZINE_LINKS_REGEX


def test_create_wanted_magazine_file_script(
    add_data_to_magazines_table,
    add_data_to_empty_test_file,
    tmp_path,
    mock_get_all_magazine_names_from_start_page_success_response,
):

    path_database, _ = add_data_to_magazines_table
    path_list_of_magazines_not_to_be_scrapped, _ = add_data_to_empty_test_file
    path_wanted_magazines = tmp_path / "wanted_magazines.txt"

    already_inserted_magazine_name = get_already_inserted_magazine_name(path_database)
    not_wanted_magazines = get_not_wanted_magazines(
        path_list_of_magazines_not_to_be_scrapped
    )
    all_magazine_names_from_start_page = get_all_magazine_names_from_start_page(
        "url", MAGAZINE_LINKS_REGEX
    )
    write_wanted_magazines_file(
        all_magazine_names_from_start_page,
        already_inserted_magazine_name,
        not_wanted_magazines,
        path_wanted_magazines,
    )

    assert path_wanted_magazines.is_file()

    with open(path_wanted_magazines) as f:
        res = f.read()
        res = res.split()
    assert res == ["Magazine_1"]
