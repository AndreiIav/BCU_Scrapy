import io

from PyPDF2 import PdfReader
import scrapy
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
from BcuSpider.itemsloaders_helpers import remove_last_element_from_url


class BCUSpider(scrapy.Spider):
    name = "bcu"
    start_urls = ["https://documente.bcucluj.ro/periodice.html"]

    wanted_magazines = [
        'Ardealul Teatral şi Artistic (1927-1928)',
        'Curierul Comercial, 1924',
        'Arhiva Someşană (1924-1940)',
    ]
    #'Ardealul Teatral şi Artistic (1927-1928)','Curierul Comercial, 1924','Arhiva Someşană (1924-1940)', 'Democraţia (1908-1913)', 'E.M.K.E (1885-1913)'
    not_wanted_magazines = [
        'Abecedar (1933-1934)',
        'Abecedar literar (1946)',
        'Afirmarea. Literară-Socială (1936-1940)',
        'Alge (1930-1931)',
        'Izraelita zsebnaptar (1943-1944)',
    ]
    magazines_without_numbers = [
        'Erdély Ev. Ref. Egyházkerület, évkönyve (1900- 1906)',
        'Curierul Agronomic, 1928',
        'Curierul Sportiv (1942-1943)',
        'Curierul Comercial, 1924',
        'Curierul Şcoalei, 1932',
        'Calendarul Asociaţiunii, Sibiu (1912-1947)',
        'Buletinul Asociaţiei Române, 1925',
        'Buletinul Ateneului Român, Oradea, 1928',
        'Crişul Repede, 1930',
        'Arhiva Someşană (1924-1940)',
        'Erdélyi Helikon (1928-1944)',
        'Dacoromania (1920-1948)',
    ]

    def parse(self, response):
        magazines = response.xpath(
            "//div//a[contains(@href, 'web/bibdigit/periodice') and not(contains(@href, '.pdf')) and normalize-space(text())]"
        )

        for mag in magazines:
            if mag.xpath("text()").get() in self.wanted_magazines:
                # if mag.xpath("text()").get() not in self.not_wanted_magazines:
                magazine = BcuMagazineLoader(item=BcuSpiderMagazineItem(), selector=mag)
                # magazine.add_xpath("magazine_name", "text()")
                # magazine.add_xpath("magazine_link", "@href")
                magazine.add_xpath("name", "text()")
                magazine.add_xpath("magazine_link", "@href")
                yield magazine.load_item()

                next_page = magazine.item.get(
                    "magazine_link"
                )  # instead of next_page = "https://documente.bcucluj.ro/" + mag.xpath("@href").get()
                if next_page:
                    yield response.follow(
                        next_page,
                        callback=self.parse_magazine_years,
                        cb_kwargs=dict(
                            # magazine_name=magazine.item.get("magazine_name"),
                            # magazine_link=magazine.item.get("magazine_link"),
                            # magazine_id=magazine.item.get(
                            #     "magazine_id", "no magazine_id"
                            # ),
                            magazine_name=magazine.item.get("name"),
                            magazine_link=magazine.item.get("magazine_link"),
                            magazine_id=magazine.item.get("magazine_id"),
                        ),
                    )

    def parse_magazine_years(self, response, magazine_name, magazine_link, magazine_id):
        magazine_years = response.xpath(
            "//a[contains(@href, 'html') and contains(text(), 'ANUL')]"
        )
        for year in magazine_years:
            magazine_year = BcuMagazineYearLoader(
                item=BcuSpiderMagazineYearItem(), selector=year
            )
            magazine_year.add_value("magazine_name", magazine_name)
            magazine_year.add_xpath("magazine_year", "text()")
            magazine_year.add_value(
                "magazine_year_link", magazine_link + year.xpath("@href").get()
            )  # magazine_year.add_xpath("magazine_year_link", "@href")
            magazine_year.add_value("magazine_id", magazine_id)
            yield magazine_year.load_item()

            next_page = magazine_year.item.get("magazine_year_link")
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse_magazine_numbers,
                    cb_kwargs=dict(
                        magazine_id=magazine_id,
                        magazine_name=magazine_name,
                        magazine_year=magazine_year.item.get("magazine_year"),
                        magazine_year_id=magazine_year.item.get("magazine_year_id"),
                        magazine_year_link=magazine_year.item.get("magazine_year_link"),
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
            magazine_year_number.add_value("magazine_name", magazine_name)
            magazine_year_number.add_value("magazine_id", magazine_id)
            year = year_number.xpath(
                ".//span[contains(@class, 'central')]/text()"
            ).get()
            link_text = year_number.xpath(
                ".//a[contains(@href, 'pdf')]/text()"
            ).getall()  # add strip()
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
                            magazine_name=magazine_year_number.item.get(
                                "magazine_name"
                            ),
                            magazine_id=magazine_year_number.item.get("magazine_id"),
                            magazine_year=magazine_year_number.item.get(
                                "magazine_year_name_without_numbers"
                            ),
                            magazine_year_id=magazine_year_number.item.get(
                                "magazine_year_id"
                            ),
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
            magazine_year_year.add_value("magazine_name", magazine_name)
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
                        magazine_name=magazine_year_year.item.get("magazine_name"),
                        magazine_id=magazine_year_year.item.get("magazine_id"),
                        magazine_year=magazine_year_year.item.get(
                            "magazine_year_name_without_numbers"
                        ),
                        magazine_year_id=magazine_year_year.item.get(
                            "magazine_year_id"
                        ),
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
        magazine_id,
        magazine_name,
        magazine_year,
        magazine_year_id,
        magazine_year_link,
        magazine_number_text="",
        magazine_without_numbers=False,
    ):
        # self.logger.info(f"In parse_magazine_numbers Response is {response.url} .")

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
                magazine_number.add_value("magazine_id", magazine_id)
                magazine_number.add_value("magazine_name", magazine_name)
                magazine_number.add_value("magazine_year", magazine_year)
                magazine_number.add_value("magazine_year_id", magazine_year_id)
                yield magazine_number.load_item()

                next_page = magazine_number.item.get("magazine_number_link")

                if next_page:
                    yield response.follow(
                        next_page,
                        callback=self.get_magazine_number_pdf,
                        cb_kwargs=dict(
                            magazine_name=magazine_number.item.get("magazine_name"),
                            magazine_id=magazine_number.item.get("magazine_id"),
                            magazine_year=magazine_number.item.get("magazine_year"),
                            magazine_year_id=magazine_number.item.get(
                                "magazine_year_id"
                            ),
                            magazine_number_text=magazine_number.item.get(
                                "magazine_number_text"
                            ),
                            magazine_number_id=magazine_number.item.get(
                                "magazine_number_id"
                            ),
                        ),
                    )

        # magazine years without numbers
        else:
            magazine_number_w = BcuMagazineNumberLoader(
                item=BcuSpiderMagazineNumberItem()
            )
            magazine_number_w.add_value("magazine_name", magazine_name)
            magazine_number_w.add_value("magazine_id", magazine_id)
            magazine_number_w.add_value("magazine_year", magazine_year)
            magazine_number_w.add_value("magazine_year_id", magazine_year_id)
            magazine_number_w.add_value("magazine_number_text", magazine_number_text)
            magazine_number_w.add_value("magazine_number_link", magazine_year_link)
            yield magazine_number_w.load_item()

            next_page = magazine_number_w.item.get("magazine_number_link")

            if next_page:
                magazine_name = magazine_number_w.item.get("magazine_name")
                magazine_id = magazine_number_w.item.get("magazine_id")
                magazine_year = magazine_number_w.item.get("magazine_year")
                magazine_year_id = magazine_number_w.item.get("magazine_year_id")
                magazine_number_text = magazine_number_w.item.get(
                    "magazine_number_text"
                )
                magazine_number_id = magazine_number_w.item.get("magazine_number_id")

                yield response.follow(
                    next_page,
                    callback=self.get_magazine_number_pdf,
                    cb_kwargs=dict(
                        magazine_name=magazine_name,
                        magazine_id=magazine_id,
                        magazine_year=magazine_year,
                        magazine_year_id=magazine_year_id,
                        magazine_number_text=magazine_number_text,
                        magazine_number_id=magazine_number_id,
                    ),
                )

    def get_magazine_number_pdf(
        self,
        response,
        magazine_name,
        magazine_id,
        magazine_year,
        magazine_year_id,
        magazine_number_text,
        magazine_number_id,
    ):
        # self.logger.info(f"In get_magazine_number_pdf Response is {response.url} .")
        # self.logger.info(f"magazine_name is {magazine_name}")
        # self.logger.info(f"magazine_id is {magazine_id}")
        # self.logger.info(f"magazine_year is {magazine_year}")
        # self.logger.info(f"magazine_year_id is {magazine_year_id}")
        # self.logger.info(f"magazine_number_text is {magazine_number_text}")
        # self.logger.info(f"magazine_number_id is {magazine_number_id}")

        bytesContent = response.body

        with io.BytesIO(bytesContent) as f:
            pdf_reader = PdfReader(f, strict=False)
            for page in range(len(pdf_reader.pages)):
                magazine_content_page = BcuMagazineContentPageLoader(
                    item=BcuSpiderMagazineContentPageItem()
                )

                p = pdf_reader.pages[page]
                magazine_content_page.add_value("magazine_name", magazine_name)
                magazine_content_page.add_value("magazine_id", magazine_id)
                magazine_content_page.add_value("magazine_year", magazine_year)
                magazine_content_page.add_value("magazine_year_id", magazine_year_id)
                magazine_content_page.add_value(
                    "magazine_number_text", magazine_number_text
                )
                magazine_content_page.add_value(
                    "magazine_number_id", magazine_number_id
                )

                magazine_content_page.add_value("magazine_content_page", page + 1)
                magazine_content_page.add_value(
                    "magazine_content_text", p.extract_text()
                )

                yield magazine_content_page.load_item()
