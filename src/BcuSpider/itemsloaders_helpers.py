import sqlite3


def remove_last_element_from_url(url):

    partition = url.rpartition("/")

    return partition[0] + partition[1]


def write_to_database(database_path, table, *values):

    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    with conn:
        if table == "magazines":
            c.execute(
                "INSERT INTO magazines(name, magazine_link) VALUES(?,?)",
                (values[0], values[1]),
            )

        if table == "magazine_year":
            c.execute(
                "INSERT INTO magazine_year(magazine_id, year, magazine_year_link) VALUES (?, ?, ?)",
                (values[0], values[1], values[2]),
            )

        if table == "magazine_number":
            c.execute(
                "INSERT INTO magazine_number(magazine_year_id, magazine_number, magazine_number_link) VALUES (?, ?, ?)",
                (values[0], values[1], values[2]),
            )

        if table == "magazine_number_content":
            c.execute(
                "INSERT INTO magazine_number_content(magazine_number_id, magazine_content, magazine_page) VALUES(?, ?, ?)",
                (values[0], values[1], values[2]),
            )

    conn.close()


def get_id_from_database(database_path, table, *values):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    if table == "magazines":
        c.execute("SELECT id FROM magazines WHERE name = ?", (values[0],))

    if table == "magazine_year":
        c.execute(
            "SELECT id FROM magazine_year WHERE magazine_id = ? AND year = ?",
            (values[0], values[1]),
        )

    if table == "magazine_number":
        c.execute(
            "SELECT id FROM magazine_number WHERE magazine_year_id = ? AND magazine_number = ?",
            (values[0], values[1]),
        )

    id = c.fetchone()[0]
    conn.close()

    return id


def get_wanted_magazines_from_file(file_path):

    try:
        with open(file_path, encoding="utf_8") as file:
            magazines = [magazine.strip() for magazine in file]
    except FileNotFoundError:
        print(
            "wanted_magazines.txt file was not found"
            f" at {file_path}. The spider has no magazine to scrape."
        )
    else:
        return magazines
