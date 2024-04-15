import pytest

import scrapy
import scrapy.exceptions
from scrapy.http import Request

from BcuSpider.spiders.main_spider import BCUSpider


@pytest.mark.parametrize("file_name", ["dummy_start_page.html"])
def test_spider_parse_content_parsed_correctly(get_html_response, create_test_tb):

    test_spider = BCUSpider()
    test_response = get_html_response
    test_spider.wanted_magazines = ["Magazine_1", "Magazine_2"]
    test_spider.path_database = create_test_tb

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
    get_html_response, create_test_tb
):

    test_spider = BCUSpider()
    test_response = get_html_response
    test_spider.wanted_magazines = ["Magazine_1"]
    test_spider.path_database = create_test_tb

    expected_dict_magazine_2 = dict(
        magazine_link="https://documente.bcucluj.ro/web/bibdigit/periodice/Magazine_2/",
        name="Magazine_2",
    )

    res = list(test_spider.parse(test_response))

    assert expected_dict_magazine_2 not in res


@pytest.mark.parametrize("file_name", ["dummy_start_page.html"])
def test_spider_parse_raised_exception_and_logged_message_if_db_is_missing(
    get_html_response, tmp_path, caplog
):

    test_spider = BCUSpider()
    test_response = get_html_response
    test_spider.path_database = tmp_path

    with pytest.raises(scrapy.exceptions.CloseSpider):
        list(test_spider.parse(test_response))

    log_message = caplog.text

    assert "CRITICAL" in log_message
    assert "Scrapper stopped" in log_message
    assert f" The .db file is not present at {test_spider.path_database}" in log_message
