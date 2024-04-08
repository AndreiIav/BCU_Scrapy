BASE_PATH = r"D:\IT projects\BCU_Scrapy_Scrapper"
DATABASE_NAME = "test.db"
START_URL_BCU = "https://documente.bcucluj.ro/periodice.html"
# Regex for extracting the correct links of the magazines found in the start page.
MAGAZINE_LINKS_REGEX = r"web/bibdigit/periodice/(.)+$"
