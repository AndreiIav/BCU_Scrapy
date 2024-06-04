import requests
import sqlite3
import re

from bs4 import BeautifulSoup


def get_already_inserted_magazine_name(path_database):
    already_inserted = []

    try:
        # This will open an existing database, but will raise an
        # error in case that file can not be opened or does not exist
        conn = sqlite3.connect(f"file:{path_database}?mode=rw", uri=True)
    except sqlite3.OperationalError as err:
        print(
            f"'sqlite3.OperationalError: {err}' error raised because"
            f" there is no database at {path_database}"
        )
    else:
        c = conn.cursor()

        with conn:
            try:
                # Check if magazines table exists in db
                result = c.execute("SELECT name FROM magazines").fetchall()
            except sqlite3.OperationalError as err:
                print(
                    f"'sqlite3.OperationalError: {err}' error raised"
                    f" in get_already_inserted_magazine_name()."
                )
            else:
                for res in result:
                    already_inserted.append(res[0])

    # if already_inserted is empty, there is no record inserted in magazines table
    # or magazines table is missing from db
    # so print a warning
    if len(already_inserted) == 0:
        print(
            f"get_already_inserted_magazine_name() returns an empty list."
            f" Check magazines table in {path_database}."
        )

    return already_inserted


def get_not_wanted_magazines(path_list_of_magazines_not_to_be_scrapped):
    not_wanted_magazines = []

    try:
        with open(path_list_of_magazines_not_to_be_scrapped, encoding="utf_8") as f:
            for line in f:
                not_wanted_magazines.append(line.strip())

            # if not_wanted_magazines is empty, the file is empty
            # so print a warning
            if len(not_wanted_magazines) == 0:
                print(
                    "get_not_wanted_magazines() returns an empty list."
                    f" Check {path_list_of_magazines_not_to_be_scrapped}"
                    " file if it is empty."
                )

    except FileNotFoundError:
        print(
            f"The 'list_of_magazines_not_to_be_scrapped.txt' does not exists at"
            f" {path_list_of_magazines_not_to_be_scrapped}"
        )

    return not_wanted_magazines


def get_all_magazine_names_from_start_page(url, regular_expression):

    magazine_names_from_start_page = []
    start_page_links_re = re.compile(regular_expression)
    warning_message = "get_all_magazine_names_from_start_page() returns an empty list."

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"{url} cannot be reached due to a HTTP Error. {warning_message}")
    except requests.exceptions.ConnectionError:
        print(f"{url} cannot be reached due to a Connection Error. {warning_message}")
    except requests.exceptions.Timeout:
        print(f"{url} cannot be reached due to a Timeout Error. {warning_message}")
    except requests.exceptions.RequestException:
        print(f"{url} cannot be reached due to a Request Exception. {warning_message}")

    else:
        soup = BeautifulSoup(r.text, "lxml")
        all_links = soup.find_all("a")

        for link in all_links:
            if link.get("href"):
                str_to_search = link.get("href")
                # get only the links that contain a magazine name
                if start_page_links_re.search(str_to_search):
                    if link.string and not link.string.isspace():
                        magazine_names_from_start_page.append(link.string.strip())

        # If magazine_names_from_start_page is empty, the html response could
        # not be parsed so print a warning.
        if len(magazine_names_from_start_page) == 0:
            print(f"the response from {url} could not be parsed. {warning_message}")

    return magazine_names_from_start_page


def write_wanted_magazines_file(
    all_magazine_names_from_start_page,
    already_inserted_magazine_name,
    not_wanted_magazines,
    path_wanted_magazines,
):

    # if path_wanted_magazines already exists, don't do anything
    # but print a warning message
    if path_wanted_magazines.is_file():
        print(
            f"{path_wanted_magazines} already exists. Remove it before attempting"
            " to create a new one."
        )
    else:
        for name in all_magazine_names_from_start_page:
            if (
                name not in already_inserted_magazine_name
                and name not in not_wanted_magazines
            ):
                with open(path_wanted_magazines, "a", encoding="utf_8") as f:
                    f.write(name + "\n")

        # check if wanted_magazines.txt file was created
        # and print a confirmation message
        if path_wanted_magazines.is_file():
            print(f"wanted_magazines.txt file was created at {path_wanted_magazines}.")
        # if the file doesn't exists there was no magazine name
        # to write in the file
        else:
            print(
                f"{path_wanted_magazines} file was not created because there was"
                " no magazine name to be written in the file."
            )
