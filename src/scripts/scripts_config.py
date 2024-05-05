import os

from dotenv import load_dotenv

load_dotenv()

BASE_PATH = os.getenv("BASE_PATH")
DATABASE_NAME = os.getenv("DATABASE_NAME")

START_URL_BCU = "https://documente.bcucluj.ro/periodice.html"
# Regex for extracting the correct links of the magazines found in the start page.
MAGAZINE_LINKS_REGEX = r"web/bibdigit/periodice/(.)+$"
