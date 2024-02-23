from utils import (
    get_already_inserted_magazine_name,
    get_not_wanted_magazines,
    get_all_magazine_names_from_start_page,
    write_wanted_magazines_file
)
from pathlib import Path

current_working_directory = Path.cwd()
path_database = current_working_directory / "BcuSpider" / "test.db"
path_list_of_magazines_not_to_be_scrapped = (current_working_directory 
                                             / "extra" 
                                             / "list_of_magazines_not_to_be_scrapped.txt"
                                             )
path_wanted_magazines = current_working_directory / "BcuSpider" / "wanted_magazines.txt"

already_inserted_magazine_name = get_already_inserted_magazine_name(
    path_database)

not_wanted_magazines = get_not_wanted_magazines(
    path_list_of_magazines_not_to_be_scrapped)

all_magazine_names_from_start_page = get_all_magazine_names_from_start_page()

write_wanted_magazines_file(all_magazine_names_from_start_page,
                            already_inserted_magazine_name,
                            not_wanted_magazines,
                            path_wanted_magazines)