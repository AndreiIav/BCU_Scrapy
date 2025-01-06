from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent
DATABASE_NAME = "app.db"
START_URL_BCU = "https://documente.bcucluj.ro/periodice.html"
# Regex for extracting the correct links of the magazines found on START_URL_BCU
MAGAZINE_LINKS_REGEX = r"web/bibdigit/periodice/(.)+$"
