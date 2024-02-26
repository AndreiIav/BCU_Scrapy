import requests
import sqlite3
import re
from bs4 import BeautifulSoup

def get_already_inserted_magazine_name(path_database):
    already_inserted = []

    try:
        #This will open an existing database, but will raise an
        #error in case that file can not be opened or does not exist
        conn = sqlite3.connect(f"file:{path_database}?mode=rw", uri=True)
    except sqlite3.OperationalError as err:
        print(f"'sqlite3.OperationalError: {err}' error raised because"
              f" there is no database at {path_database}")
    else:
        c = conn.cursor()

        with conn:
            try:
                result = c.execute("SELECT name FROM magazines").fetchall()
            except sqlite3.OperationalError as err:
                    print(f"'sqlite3.OperationalError: {err}' error raised.")
            else:
                for res in result:
                    already_inserted.append(res[0])

    return already_inserted


def get_not_wanted_magazines(path_list_of_magazines_not_to_be_scrapped):
    not_wanted_magazines = []

    try:
        with open(path_list_of_magazines_not_to_be_scrapped, encoding="utf_8") as f:
            for line in f:
                not_wanted_magazines.append(line.strip())
    except FileNotFoundError:
        print(f"The 'list_of_magazines_not_to_be_scrapped.txt' does not exists at"
              f" {path_list_of_magazines_not_to_be_scrapped}")

    return not_wanted_magazines


def get_all_magazine_names_from_start_page():

    magazine_names_from_start_page = []

    # Regex for extracting the correct links of the magazines found
    # in the start page.
    start_page_links_re = re.compile(r"web/bibdigit/periodice/(.)+$")

    r = requests.get("https://documente.bcucluj.ro/periodice.html")
    r.raise_for_status
    soup = BeautifulSoup(r.text, "lxml")
    all_links = soup.find_all("a")

    for link in all_links:
        if link.get("href"):
            str_to_search = link.get("href")
            # get only the links that contain a magazine name
            if start_page_links_re.search(str_to_search):
                if link.string and not link.string.isspace():
                    magazine_names_from_start_page.append(link.string)

    return magazine_names_from_start_page


def write_wanted_magazines_file(all_magazine_names_from_start_page,
                                already_inserted_magazine_name,
                                not_wanted_magazines,
                                path_wanted_magazines):

    for name in all_magazine_names_from_start_page:
        if (name not in already_inserted_magazine_name and
            name not in not_wanted_magazines
            ):
            with open(path_wanted_magazines, "a", encoding="utf_8") as f:
                f.write(name + "\n")

    # check if wanted_magazines.txt file was created
    # and print a confirmation message
    if path_wanted_magazines.is_file():
        print("wanted_magazines.txt file was created.")
    # if the file doesn't exists there was no magazine name
    # to write in the file
    else:
        print("wanted_magazines.txt file was not created because there was"
              " no magazine name to be written in the file.")