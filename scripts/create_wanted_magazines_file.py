from pathlib import Path

from utils import (
    get_already_inserted_magazine_name,
    get_not_wanted_magazines,
    get_all_magazine_names_from_start_page,
    write_wanted_magazines_file,
)
from scripts.scripts_config import BASE_PATH, DATABASE_NAME

path_database = Path(BASE_PATH) / "BcuSpider" / DATABASE_NAME
path_list_of_magazines_not_to_be_scrapped = (
    Path(BASE_PATH) / "extra" / "list_of_magazines_not_to_be_scrapped.txt"
)
path_wanted_magazines = Path(BASE_PATH) / "BcuSpider" / "wanted_magazines.txt"

already_inserted_magazine_name = get_already_inserted_magazine_name(path_database)

not_wanted_magazines = get_not_wanted_magazines(
    path_list_of_magazines_not_to_be_scrapped
)

all_magazine_names_from_start_page = get_all_magazine_names_from_start_page()

write_wanted_magazines_file(
    all_magazine_names_from_start_page,
    already_inserted_magazine_name,
    not_wanted_magazines,
    path_wanted_magazines,
)
