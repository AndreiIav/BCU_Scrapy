import pytest

import scrapy
import scrapy.exceptions
from scrapy.http import Request

from BcuSpider.spiders.main_spider import BCUSpider


class TestSpiderParseStartPage:

    @pytest.mark.parametrize("file_name", ["dummy_start_page.html"])
    def test_spider_parse_content_parsed_correctly(
        self, get_html_response, create_test_db
    ):

        test_spider = BCUSpider()
        test_response = get_html_response
        test_spider.wanted_magazines = ["Magazine_1", "Magazine_2"]
        test_spider.path_database = create_test_db

        expected_dict_magazine_1 = dict(
            magazine_link="https://documente.bcucluj.ro/web/bibdigit/periodice/Magazine_1/",
            name="Magazine_1",
        )
        expected_request_magazine_1 = Request(
            url="https://documente.bcucluj.ro/web/bibdigit/periodice/Magazine_1/"
        )

        expected_dict_magazine_2 = dict(
            magazine_link="https://documente.bcucluj.ro/web/bibdigit/periodice/Magazine_2/",
            name="Magazine_2",
        )
        expected_request_magazine_2 = Request(
            url="https://documente.bcucluj.ro/web/bibdigit/periodice/Magazine_2/"
        )

        res = list(test_spider.parse(test_response))

        assert expected_dict_magazine_1 in res
        assert expected_request_magazine_1.url == res[1].url
        assert expected_request_magazine_1.method == res[1].method

        assert expected_dict_magazine_2 in res
        assert expected_request_magazine_2.url == res[3].url
        assert expected_request_magazine_2.method == res[3].method

    @pytest.mark.parametrize("file_name", ["dummy_start_page.html"])
    def test_spider_parse_not_wanted_magazine_not_scrapped(
        self, get_html_response, create_test_db
    ):

        test_spider = BCUSpider()
        test_response = get_html_response
        test_spider.wanted_magazines = ["Magazine_1"]
        test_spider.path_database = create_test_db

        expected_dict_magazine_2 = dict(
            magazine_link="https://documente.bcucluj.ro/web/bibdigit/periodice/Magazine_2/",
            name="Magazine_2",
        )

        res = list(test_spider.parse(test_response))

        assert expected_dict_magazine_2 not in res

    @pytest.mark.parametrize("file_name", ["dummy_start_page.html"])
    def test_spider_parse_raised_exception_and_logged_message_if_db_is_missing(
        self, get_html_response, tmp_path, caplog
    ):

        test_spider = BCUSpider()
        test_response = get_html_response
        test_spider.path_database = tmp_path

        with pytest.raises(scrapy.exceptions.CloseSpider):
            list(test_spider.parse(test_response))

        log_message = caplog.text

        assert "CRITICAL" in log_message
        assert "Scrapper stopped" in log_message
        assert (
            f" The .db file is not present at {test_spider.path_database}"
            in log_message
        )


class TestSpiderParseMagazineYears:

    @pytest.mark.parametrize("file_name", ["dummy_magazine_years_page.html"])
    def test_spider_parse_magazine_years_content_parsed_correctly(
        self, get_html_response
    ):

        test_spider = BCUSpider()
        test_response = get_html_response
        magazine_link = "https://www.mag_link/"
        magazine_id = 1

        expected_dict_magazine = dict(
            magazine_year_link=f"{magazine_link}1900.html",
            year="ANUL 1900",
            magazine_id=magazine_id,
        )
        expected_request_magazine = Request(url=f"{magazine_link}1900.html")

        res = list(
            test_spider.parse_magazine_years(test_response, magazine_link, magazine_id)
        )

        assert expected_dict_magazine == res[0]
        assert expected_request_magazine.url == res[1].url
        assert expected_request_magazine.method == res[1].method

    @pytest.mark.parametrize(
        "file_name", ["dummy_magazine_years_page_multiple_magazine_links.html"]
    )
    def test_spider_parse_magazine_years_with_multiple_links_content_parsed_correctly(
        self, get_html_response
    ):

        test_spider = BCUSpider()
        test_response = get_html_response
        magazine_link = "https://www.mag_link/"
        magazine_id = 1

        expected_dict_magazine = dict(
            magazine_id=magazine_id,
            magazine_year_name_without_numbers="ANUL 1901",
            magazine_year_number=[
                ("A", "https://www.mag_link/A.pdf"),
                ("B", "https://www.mag_link/B.pdf"),
            ],
        )
        expected_request_magazine_1 = Request(url=f"{magazine_link}A.pdf")
        expected_request_magazine_2 = Request(url=f"{magazine_link}B.pdf")

        res = list(
            test_spider.parse_magazine_years(test_response, magazine_link, magazine_id)
        )

        assert expected_dict_magazine == res[0]

        assert expected_request_magazine_1.url == res[1].url
        assert expected_request_magazine_1.method == res[1].method

        assert expected_request_magazine_2.url == res[2].url
        assert expected_request_magazine_2.method == res[2].method

    @pytest.mark.parametrize(
        "file_name", ["dummy_magazine_years_page_one_magazine_link.html"]
    )
    def test_spider_parse_magazine_years_with_one_link_content_parsed_correctly(
        self, get_html_response
    ):

        test_spider = BCUSpider()
        test_response = get_html_response
        magazine_link = "https://www.mag_link/"
        magazine_id = 1

        expected_dict_magazine = dict(
            magazine_id=magazine_id,
            magazine_year_name_without_numbers="ANUL 1902",
            magazine_year_link=f"{magazine_link}year_mag_link.pdf",
        )
        expected_request_magazine = Request(url=f"{magazine_link}year_mag_link.pdf")

        res = list(
            test_spider.parse_magazine_years(test_response, magazine_link, magazine_id)
        )

        assert expected_dict_magazine in res
        assert expected_request_magazine.url == res[1].url
        assert expected_request_magazine.method == res[1].method

    class TestSpiderParseMagazineNumbers:

        @pytest.mark.parametrize("file_name", ["dummy_magazine_numbers_page.html"])
        def test_parse_magazine_numbers_content_parsed_correctly(
            self, get_html_response
        ):

            test_spider = BCUSpider()
            test_response = get_html_response
            magazine_year_id = 1
            magazine_year_link = "https://www.mag_link/1900.html"

            expected_dict_magazine = dict(
                magazine_number_text="Nr.1",
                magazine_number_link="https://www.mag_link/01.pdf",
                magazine_year_id=magazine_year_id,
            )

            res = list(
                test_spider.parse_magazine_numbers(
                    test_response, magazine_year_id, magazine_year_link
                )
            )
            expected_next_request = Request(url="https://www.mag_link/01.pdf")

            assert expected_dict_magazine in res

            assert expected_next_request.url == res[1].url
            assert expected_next_request.method == res[1].method

        # regression test
        @pytest.mark.parametrize(
            "file_name", ["dummy_magazine_numbers_page_without_div_bug.html"]
        )
        def test_parse_magazine_numbers_without_div_content_parsed_correctly(
            self, get_html_response
        ):

            test_spider = BCUSpider()
            test_response = get_html_response
            magazine_year_id = 1
            magazine_year_link = "https://www.mag_link/1900.html"

            expected_dict_magazine = dict(
                magazine_number_text="Nr.1",
                magazine_number_link="https://www.mag_link/01.pdf",
                magazine_year_id=magazine_year_id,
            )

            res = list(
                test_spider.parse_magazine_numbers(
                    test_response, magazine_year_id, magazine_year_link
                )
            )
            expected_next_request = Request(url="https://www.mag_link/01.pdf")

            assert expected_dict_magazine in res

            assert expected_next_request.url == res[1].url
            assert expected_next_request.method == res[1].method

        @pytest.mark.parametrize("file_name", ["dummy_magazine_numbers_page.html"])
        def test_parse_magazine_numbers_for_magazines_without_numbers_success(
            self, get_html_response
        ):

            test_spider = BCUSpider()
            test_response = get_html_response
            magazine_year_id = 1
            magazine_number_text = "Nr.1"
            magazine_year_link = "https://www.mag_link/1900.html"

            expected_dict_magazine = dict(
                magazine_year_id=magazine_year_id,
                magazine_number_text=magazine_number_text,
                magazine_number_link=magazine_year_link,
            )
            expected_next_request = Request(url=magazine_year_link)

            res = list(
                test_spider.parse_magazine_numbers(
                    test_response,
                    magazine_year_id,
                    magazine_year_link,
                    magazine_number_text,
                    magazine_without_numbers=True,
                )
            )

            assert expected_dict_magazine in res

            assert expected_next_request.url == res[1].url
            assert expected_next_request.method == res[1].method

    class TestSpiderGetMagazineNumberPdf:

        @pytest.mark.parametrize("file_name", ["test.pdf"])
        def test_get_magazine_number_pdf_success(self, get_html_response):

            test_spider = BCUSpider()
            test_response = get_html_response
            magazine_number_id = 1
            magazine_content_page = 1

            expected_res = dict(
                magazine_number_id=magazine_number_id,
                magazine_content_page=magazine_content_page,
                magazine_content_text="test pdf\ntest pdf1\ntest pdf2",
            )

            res = list(
                test_spider.get_magazine_number_pdf(test_response, magazine_number_id)
            )

            assert expected_res in res
