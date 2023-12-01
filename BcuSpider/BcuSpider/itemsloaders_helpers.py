import sqlite3


class IncrementId:
    counter = 0

    @classmethod
    def increment_on_call(cls, y=1):
        cls.counter += y
        return cls.counter

    @classmethod
    def reset_counter(cls):
        cls.counter = 0


def remove_last_element_from_url(url):
    partition = url.rpartition("/")
    return partition[0] + partition[1]


def write_to_database(database_name, table, *values):
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = 1")  # to enable foreign keys
    c = conn.cursor()

    with conn:
        # magazines table
        if table == "magazines":
            c.execute(
                "INSERT INTO magazines(name, magazine_link) VALUES(?,?)",
                (values[0], values[1]),
            )

        # magazine_year table
        if table == "magazine_year":
            c.execute(
                "INSERT INTO magazine_year(magazine_id, year, magazine_year_link) VALUES (?, ?, ?)",
                (values[0], values[1], values[2]),
            )

        # magazine_number table
        if table == "magazine_number":
            c.execute(
                "INSERT INTO magazine_number(magazine_year_id, magazine_number, magazine_number_link) VALUES (?, ?, ?)",
                (values[0], values[1], values[2]),
            )

        # magazine_number_content
        if table == "magazine_number_content":
            c.execute(
                "INSERT INTO magazine_number_content(magazine_number_id, magazine_content, magazine_page) VALUES(?, ?, ?)",
                (values[0], values[1], values[2]),
            )

    conn.close()


def get_id_from_database(database_name, table, *values):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    # magazines table
    if table == "magazines":
        c.execute("SELECT id FROM magazines WHERE name = ?", (values[0],))

    # magazine_year table
    if table == "magazine_year":
        c.execute(
            "SELECT id FROM magazine_year WHERE magazine_id = ? AND year = ?",
            (values[0], values[1]),
        )

    # magazine_number table
    if table == "magazine_number":
        c.execute(
            "SELECT id FROM magazine_number WHERE magazine_year_id = ? AND magazine_number = ?",
            (values[0], values[1]),
        )

    id = c.fetchone()[0]
    conn.close()

    return id
