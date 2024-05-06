import io
import sqlite3
import logging
from pathlib import Path

import scrapy
from pypdf import PdfReader

from BcuSpider.items import (
    BcuSpiderMagazineItem,
    BcuSpiderMagazineYearItem,
    BcuSpiderMagazineNumberItem,
    BcuSpiderMagazineYearWithoutNumbersItem,
    BcuSpiderMagazineContentPageItem,
)
from BcuSpider.itemsloaders import (
    BcuMagazineLoader,
    BcuMagazineYearLoader,
    BcuMagazineNumberLoader,
    BcuMagazineYearWithoutNumbersLoader,
    BcuMagazineContentPageLoader,
)
from BcuSpider.itemsloaders_helpers import (
    remove_last_element_from_url,
    get_wanted_magazines_from_file,
)

from scripts.scripts_config import (
    BASE_PATH,
    START_URL_BCU,
    DATABASE_NAME,
)


class BCUSpider(scrapy.Spider):
    name = "bcu"
    start_urls = [START_URL_BCU]
    path_database = Path(BASE_PATH) / DATABASE_NAME
    path_wanted_magazines_file = Path(BASE_PATH) / "wanted_magazines.txt"
    wanted_magazines = get_wanted_magazines_from_file(path_wanted_magazines_file)

    def parse(self, response):

        # check if database file exists
        # if not, close the spider
        path_database = self.path_database
        try:
            # This will open an existing database, but will raise an
            # error in case that file can not be opened or does not exist
            conn = sqlite3.connect(f"file:{path_database}?mode=rw", uri=True)
        except sqlite3.OperationalError as e:
            logging.critical(
                f"Scrapper stopped because 'sqlite3.OperationalError: {e}'"
                f" error was raised."
                f" The .db file is not present at {path_database}"
            )
            raise scrapy.exceptions.CloseSpider()
        else:
            conn.close()

        magazines = response.xpath(
            "//div//a[contains(@href, 'web/bibdigit/periodice') and"
            " not(contains(@href, '.pdf')) and normalize-space(text())]"
        )

        for mag in magazines:
            if mag.xpath("text()").get() in self.wanted_magazines:
                magazine = BcuMagazineLoader(item=BcuSpiderMagazineItem(), selector=mag)
                magazine.add_xpath("name", "text()")
                magazine.add_xpath("magazine_link", "@href")
                yield magazine.load_item()

                next_page = magazine.item.get("magazine_link")
                if next_page:
                    yield response.follow(
                        next_page,
                        callback=self.parse_magazine_years,
                        cb_kwargs=dict(
                            magazine_link=magazine.item.get("magazine_link"),
                            magazine_id=magazine.item.get("id"),
                        ),
                    )

    def parse_magazine_years(self, response, magazine_link, magazine_id):
        magazine_years = response.xpath(
            "//a[contains(@href, 'html') and contains(text(), 'ANUL')]"
        )
        for year in magazine_years:
            magazine_year = BcuMagazineYearLoader(
                item=BcuSpiderMagazineYearItem(), selector=year
            )

            magazine_year.add_xpath("year", "text()")
            magazine_year.add_value(
                "magazine_year_link", magazine_link + year.xpath("@href").get()
            )
            magazine_year.add_value("magazine_id", magazine_id)
            yield magazine_year.load_item()

            next_page = magazine_year.item.get("magazine_year_link")
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse_magazine_numbers,
                    cb_kwargs=dict(
                        magazine_year_link=magazine_year.item.get("magazine_year_link"),
                        magazine_year_id=magazine_year.item.get("id"),
                    ),
                )

        # magazine_years that have multiple magazine links
        magazine_years_numbers = response.xpath(
            "//tr//td[contains(@background, '.jpg')]//div[contains(@align, 'left')]"
        )
        for year_number in magazine_years_numbers:
            magazine_year_number = BcuMagazineYearWithoutNumbersLoader(
                item=BcuSpiderMagazineYearWithoutNumbersItem(), selector=year_number
            )
            magazine_year_number.add_value("magazine_id", magazine_id)
            year = year_number.xpath(
                ".//span[contains(@class, 'central')]/text()"
            ).get()
            link_text = year_number.xpath(
                ".//a[contains(@href, 'pdf')]/text()"
            ).getall()
            links = year_number.xpath(".//a[contains(@href, 'pdf')]/@href").getall()
            links = [magazine_link + link for link in links]
            res = [list(zip(link_text, links))]
            magazine_year_number.add_value("magazine_year_name_without_numbers", year)
            magazine_year_number.add_value("magazine_year_number", res)
            yield magazine_year_number.load_item()

            for link_text, next_page in magazine_year_number.item.get(
                "magazine_year_number"
            ):
                if next_page:
                    yield response.follow(
                        next_page,
                        callback=self.parse_magazine_numbers,
                        cb_kwargs=dict(
                            magazine_year_id=magazine_year_number.item.get("id"),
                            magazine_year_link=next_page,
                            magazine_number_text=link_text.strip(),
                            magazine_without_numbers=True,
                        ),
                    )

        # magazine_years that have a single magazine link
        magazine_years_year = response.xpath(
            "//tr//td[contains(@background, '.jpg')]//div[contains(@align, 'center')]//a[contains(@href, '.pdf')]"
        )
        for year_year in magazine_years_year:
            magazine_year_year = BcuMagazineYearWithoutNumbersLoader(
                item=BcuSpiderMagazineYearWithoutNumbersItem(), selector=year_year
            )
            magazine_year_year.add_value("magazine_id", magazine_id)
            magazine_year_year.add_xpath("magazine_year_name_without_numbers", "text()")
            magazine_year_year.add_value(
                "magazine_year_link", magazine_link + year_year.xpath("@href").get()
            )
            yield magazine_year_year.load_item()

            next_page = magazine_year_year.item.get("magazine_year_link")
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse_magazine_numbers,
                    cb_kwargs=dict(
                        magazine_year_id=magazine_year_year.item.get("id"),
                        magazine_year_link=magazine_year_year.item.get(
                            "magazine_year_link"
                        ),
                        magazine_number_text=magazine_year_year.item.get(
                            "magazine_year_name_without_numbers"
                        ),
                        magazine_without_numbers=True,
                    ),
                )

    def parse_magazine_numbers(
        self,
        response,
        magazine_year_id,
        magazine_year_link,
        magazine_number_text="",
        magazine_without_numbers=False,
    ):
        if not magazine_without_numbers:
            magazine_numbers = response.xpath(
                "//div//a[contains(@href, '.pdf') and normalize-space(text())]"
            )

            for number in magazine_numbers:
                magazine_number = BcuMagazineNumberLoader(
                    item=BcuSpiderMagazineNumberItem(), selector=number
                )
                magazine_number.add_xpath("magazine_number_text", "text()")
                magazine_number.add_value(
                    "magazine_number_link",
                    remove_last_element_from_url(magazine_year_link)
                    + number.xpath("@href").get(),
                )
                magazine_number.add_value("magazine_year_id", magazine_year_id)
                yield magazine_number.load_item()

                next_page = magazine_number.item.get("magazine_number_link")

                if next_page:
                    yield response.follow(
                        next_page,
                        callback=self.get_magazine_number_pdf,
                        cb_kwargs=dict(
                            magazine_number_id=magazine_number.item.get("id"),
                        ),
                    )

        # magazine years without numbers
        else:
            magazine_number_w = BcuMagazineNumberLoader(
                item=BcuSpiderMagazineNumberItem()
            )
            magazine_number_w.add_value("magazine_year_id", magazine_year_id)
            magazine_number_w.add_value("magazine_number_text", magazine_number_text)
            magazine_number_w.add_value("magazine_number_link", magazine_year_link)
            yield magazine_number_w.load_item()

            next_page = magazine_number_w.item.get("magazine_number_link")

            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.get_magazine_number_pdf,
                    cb_kwargs=dict(magazine_number_id=magazine_number_w.item.get("id")),
                )

    def get_magazine_number_pdf(
        self,
        response,
        magazine_number_id,
    ):
        bytesContent = response.body

        with io.BytesIO(bytesContent) as f:
            pdf_reader = PdfReader(f, strict=False)
            for page in range(len(pdf_reader.pages)):
                magazine_content_page = BcuMagazineContentPageLoader(
                    item=BcuSpiderMagazineContentPageItem()
                )

                p = pdf_reader.pages[page]
                magazine_content_page.add_value(
                    "magazine_number_id", magazine_number_id
                )

                magazine_content_page.add_value("magazine_content_page", page + 1)
                magazine_content_page.add_value(
                    "magazine_content_text", p.extract_text()
                )

                yield magazine_content_page.load_item()
