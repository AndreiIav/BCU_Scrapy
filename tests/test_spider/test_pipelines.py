import sqlite3

import pytest
from scrapy.exceptions import DropItem

from BcuSpider.items import (
    BcuSpiderMagazineItem,
    BcuSpiderMagazineYearItem,
    BcuSpiderMagazineYearWithoutNumbersItem,
    BcuSpiderMagazineNumberItem,
    BcuSpiderMagazineContentPageItem,
)
from BcuSpider.pipelines import (
    BcuMagazinesPipeline,
    BcuMagazineYearsPipeline,
    BcuMagazineYearsWithoutNumbersPipeline,
    BcuMagazineNumbersPipeline,
    BcuNumberPageContentPipeline,
)
from BcuSpider.spiders.main_spider import BCUSpider


class TestBcuMagazinesPipeline:

    def test_magazines_pipeline_data_is_written_in_database(self, create_db_tables):
        """
        When a BcuSpiderMagazineItem is processed the attributes of the item
        should be inserted in a database in magazines table.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineItem()
        test_item["name"] = "Test_Magazine_Name"
        test_item["magazine_link"] = "Test_Link"
        test_pipeline = BcuMagazinesPipeline()
        test_pipeline.path_database = create_db_tables

        test_pipeline.process_item(test_item, test_spider)

        conn = sqlite3.connect(test_pipeline.path_database)
        c = conn.cursor()
        with conn:
            inserted_magazine_name = c.execute("SELECT name from magazines").fetchone()[
                0
            ]
            inserted_magazine_link = c.execute(
                "SELECT magazine_link from magazines"
            ).fetchone()[0]
            inserted_id = c.execute("SELECT id from magazines").fetchone()

        assert inserted_magazine_name == test_item["name"]
        assert inserted_magazine_link == test_item["magazine_link"]
        assert inserted_id is not None

    def test_magazines_pipeline_with_correct_attributes(self, create_db_tables):
        """
        When a BcuSpiderMagazineItem is processed the returned item should have
        the same attributes as the one processed plus an id attribute.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineItem()
        test_item["name"] = "Test_Magazine_Name"
        test_item["magazine_link"] = "Test_Link"
        test_pipeline = BcuMagazinesPipeline()
        test_pipeline.path_database = create_db_tables

        res = test_pipeline.process_item(test_item, test_spider)

        assert res["name"] == test_item["name"]
        assert res["magazine_link"] == test_item["magazine_link"]
        assert res["id"] != 0

    def test_magazines_pipeline_with_different_item_type(self):
        """
        When an item different than BcuSpiderMagazineItem is processed the
        returned item should have the same attributes as the one processed
        and no additional one.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearItem()
        test_item["magazine_id"] = 1
        test_item["year"] = "Test_Year"
        test_item["magazine_year_link"] = "Test_Magazine_Year"
        test_pipeline = BcuMagazinesPipeline()

        res = test_pipeline.process_item(test_item, test_spider)

        assert len(res.keys()) == 3
        assert res["magazine_id"] == test_item["magazine_id"]
        assert res["year"] == test_item["year"]
        assert res["magazine_year_link"] == test_item["magazine_year_link"]


class TestBcuMagazineYearsPipeline:

    def test_magazine_years_pipeline_data_is_written_in_database(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineYearItem is processed the attributes of the item
        should be inserted in a database in magazine_year table.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearItem()
        test_item["magazine_id"] = 1
        test_item["year"] = "Test_Year"
        test_item["magazine_year_link"] = "Test_Magazine_Year"
        test_pipeline = BcuMagazineYearsPipeline()
        test_pipeline.path_database = create_db_tables

        test_pipeline.process_item(test_item, test_spider)

        conn = sqlite3.connect(test_pipeline.path_database)
        c = conn.cursor()
        with conn:
            inserted_magazine_id = c.execute(
                "SELECT magazine_id from magazine_year"
            ).fetchone()[0]
            inserted_magazine_year = c.execute(
                "SELECT year from magazine_year"
            ).fetchone()[0]
            inserted_magazine_year_link = c.execute(
                "SELECT magazine_year_link from magazine_year"
            ).fetchone()[0]
            inserted_id = c.execute("SELECT id from magazine_year").fetchone()

        assert inserted_magazine_id == test_item["magazine_id"]
        assert inserted_magazine_year == test_item["year"]
        assert inserted_magazine_year_link == test_item["magazine_year_link"]
        assert inserted_id is not None

    def test_magazine_years_pipeline_correct_attributes(self, create_db_tables):
        """
        When a BcuSpiderMagazineYearItem is processed the returned item should have
        the same attributes as the one processed plus an id attribute.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearItem()
        test_item["magazine_id"] = "Test_Magazine_id"
        test_item["year"] = "Test_Year"
        test_item["magazine_year_link"] = "Test_Magazine_Year_Link"
        test_pipeline = BcuMagazineYearsPipeline()
        test_pipeline.path_database = create_db_tables

        res = test_pipeline.process_item(test_item, test_spider)

        assert res["magazine_id"] == test_item["magazine_id"]
        assert res["year"] == test_item["year"]
        assert res["magazine_year_link"] == test_item["magazine_year_link"]
        assert res["id"] != 0

    def test_magazine_years_pipeline_with_different_item_type(self):
        """
        When an item different than BcuSpiderMagazineYearItem is processed the
        returned item should have the same attributes as the one processed
        and no additional one.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineItem()
        test_item["name"] = "Test_Magazine_Name"
        test_item["magazine_link"] = "Test_Link"
        test_pipeline = BcuMagazineYearsPipeline()

        res = test_pipeline.process_item(test_item, test_spider)

        assert len(res.keys()) == 2
        assert res["name"] == test_item["name"]
        assert res["magazine_link"] == test_item["magazine_link"]


class TestBcuMagazineYearsWithoutNumbersPipeline:

    def test_magazine_years_without_numbers_with_multiple_magazine_links_is_written_in_database(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineYearWithoutNumbersItem is processed and the item
        has multiple magazine links the attributes of the item should be
        inserted in a database in magazine_year table.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearWithoutNumbersItem()
        test_item["magazine_id"] = 1
        test_item["magazine_year_number"] = [
            ("Partea 1", "Partea_1_link"),
            ("Partea 2", "Partea_2_link"),
        ]
        test_item["magazine_year_name_without_numbers"] = "Test_Magazine_Year_Number"
        test_pipeline = BcuMagazineYearsWithoutNumbersPipeline()
        test_pipeline.path_database = create_db_tables

        test_pipeline.process_item(test_item, test_spider)

        conn = sqlite3.connect(test_pipeline.path_database)
        c = conn.cursor()
        with conn:
            inserted_magazine_id = c.execute(
                "SELECT magazine_id from magazine_year"
            ).fetchone()[0]
            inserted_magazine_year = c.execute(
                "SELECT year from magazine_year"
            ).fetchone()[0]
            inserted_magazine_year_link = c.execute(
                "SELECT magazine_year_link from magazine_year"
            ).fetchone()[0]
            inserted_id = c.execute("SELECT id from magazine_year").fetchone()

        assert inserted_magazine_id == test_item["magazine_id"]
        assert inserted_magazine_year == test_item["magazine_year_name_without_numbers"]
        assert inserted_magazine_year_link == str(test_item["magazine_year_number"])
        assert inserted_id is not None

    def test_magazine_years_without_numbers_with_multiple_magazine_links_correct_attributes(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineYearWithoutNumbersItem is processed and the item
        has multiple magazine links the returned item should have the same
        attributes as the one processed plus an id attribute.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearWithoutNumbersItem()
        test_item["magazine_id"] = 1
        test_item["magazine_year_number"] = [
            ("Partea 1", "Partea_1_link"),
            ("Partea 2", "Partea_2_link"),
        ]
        test_item["magazine_year_name_without_numbers"] = "Test_Magazine_Year_Number"
        test_pipeline = BcuMagazineYearsWithoutNumbersPipeline()
        test_pipeline.path_database = create_db_tables

        res = test_pipeline.process_item(test_item, test_spider)

        assert res["magazine_id"] == test_item["magazine_id"]
        assert (
            res["magazine_year_name_without_numbers"]
            == test_item["magazine_year_name_without_numbers"]
        )
        assert res["magazine_year_number"] == test_item["magazine_year_number"]
        assert res["id"] is not None

    def test_magazine_years_without_numbers_with_a_single_magazine_link_is_written_in_database(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineYearWithoutNumbersItem is processed and the item
        has a single magazine link the attributes of the item should be inserted
        in a database in magazine_year table.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearWithoutNumbersItem()
        test_item["magazine_id"] = 1
        test_item["magazine_year_name_without_numbers"] = "Test_Magazine_Year_Number"
        test_item["magazine_year_link"] = "Test_Magazine_Year_Link"
        test_pipeline = BcuMagazineYearsWithoutNumbersPipeline()
        test_pipeline.path_database = create_db_tables

        test_pipeline.process_item(test_item, test_spider)

        conn = sqlite3.connect(test_pipeline.path_database)
        c = conn.cursor()
        with conn:
            inserted_magazine_id = c.execute(
                "SELECT magazine_id from magazine_year"
            ).fetchone()[0]
            inserted_magazine_year = c.execute(
                "SELECT year from magazine_year"
            ).fetchone()[0]
            inserted_magazine_year_link = c.execute(
                "SELECT magazine_year_link from magazine_year"
            ).fetchone()[0]
            inserted_id = c.execute("SELECT id from magazine_year").fetchone()

        assert inserted_magazine_id == test_item["magazine_id"]
        assert inserted_magazine_year == test_item["magazine_year_name_without_numbers"]
        assert inserted_magazine_year_link == test_item["magazine_year_link"]
        assert inserted_id is not None

    def test_magazine_years_without_numbers_with_a_single_magazine_link_correct_attributes(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineYearWithoutNumbersItem is processed and the item
        has a single magazine link the returned item should have the same
        attributes as the one processed plus an id attribute.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineYearWithoutNumbersItem()
        test_item["magazine_id"] = 1
        test_item["magazine_year_name_without_numbers"] = "Test_Magazine_Year_Number"
        test_item["magazine_year_link"] = "Test_Magazine_Year_Link"
        test_pipeline = BcuMagazineYearsWithoutNumbersPipeline()
        test_pipeline.path_database = create_db_tables

        res = test_pipeline.process_item(test_item, test_spider)

        assert res["magazine_id"] == test_item["magazine_id"]
        assert (
            res["magazine_year_name_without_numbers"]
            == test_item["magazine_year_name_without_numbers"]
        )
        assert res["magazine_year_link"] == test_item["magazine_year_link"]
        assert res["id"] is not None

    def test_magazine_years_without_numbers_pipeline_with_different_item_type(self):
        """
        When an item different than BcuSpiderMagazineYearWithoutNumbersItem is
        processed the returned item should have the same attributes as the one
        processed and no additional one.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineItem()
        test_item["name"] = "Test_Magazine_Name"
        test_item["magazine_link"] = "Test_Link"
        test_pipeline = BcuMagazineYearsWithoutNumbersPipeline()

        res = test_pipeline.process_item(test_item, test_spider)

        assert len(res.keys()) == 2
        assert res["name"] == test_item["name"]
        assert res["magazine_link"] == test_item["magazine_link"]


class TestBcuMagazineNumbersPipeline:

    def test_magazine_numbers_pipeline_data_is_written_in_database(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineNumberItem is processed the attributes of the
        item should be inserted in a database in magazine_number table.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineNumberItem()
        test_item["magazine_year_id"] = 1
        test_item["magazine_number_text"] = "Test_Magazine_Number_Text"
        test_item["magazine_number_link"] = "Test_Magazine_Number_Link"
        test_pipeline = BcuMagazineNumbersPipeline()
        test_pipeline.path_database = create_db_tables

        test_pipeline.process_item(test_item, test_spider)

        conn = sqlite3.connect(test_pipeline.path_database)
        c = conn.cursor()
        with conn:
            inserted_magazine_year_id = c.execute(
                "SELECT magazine_year_id from magazine_number"
            ).fetchone()[0]
            inserted_magazine_number_text = c.execute(
                "SELECT magazine_number from magazine_number"
            ).fetchone()[0]
            inserted_magazine_number_link = c.execute(
                "SELECT magazine_number_link from magazine_number"
            ).fetchone()[0]
            inserted_id = c.execute("SELECT id from magazine_number").fetchone()

        assert inserted_magazine_year_id == test_item["magazine_year_id"]
        assert inserted_magazine_number_text == test_item["magazine_number_text"]
        assert inserted_magazine_number_link == test_item["magazine_number_link"]
        assert inserted_id is not None

    def test_magazine_numbers_pipeline_correct_attributes(self, create_db_tables):
        """
        When a BcuSpiderMagazineNumberItem is processed the returned item
        should have the same attributes as the one processed plus an id
        attribute.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineNumberItem()
        test_item["magazine_year_id"] = 1
        test_item["magazine_number_text"] = "Test_Magazine_Number_Text"
        test_item["magazine_number_link"] = "Test_Magazine_Number_Link"
        test_pipeline = BcuMagazineNumbersPipeline()
        test_pipeline.path_database = create_db_tables

        res = test_pipeline.process_item(test_item, test_spider)

        assert res["magazine_year_id"] == test_item["magazine_year_id"]
        assert res["magazine_number_text"] == test_item["magazine_number_text"]
        assert res["magazine_number_link"] == test_item["magazine_number_link"]
        assert res["id"] is not None

    def test_magazine_number_pipeline_with_different_item_type(self):
        """
        When an item different than BcuSpiderMagazineNumberItem is processed the
        returned item should have the same attributes as the one processed and
        no additional one.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineItem()
        test_item["name"] = "Test_Magazine_Name"
        test_item["magazine_link"] = "Test_Link"
        test_pipeline = BcuMagazineNumbersPipeline()

        res = test_pipeline.process_item(test_item, test_spider)

        assert len(res.keys()) == 2
        assert res["name"] == test_item["name"]
        assert res["magazine_link"] == test_item["magazine_link"]

    def test_magazine_number_pipeline_drop_item_due_to_incorect_magazine_number_link(
        self,
    ):

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineNumberItem()
        test_item["magazine_year_id"] = 1
        test_item["magazine_number_text"] = "Test_Magazine_Number_Text"
        test_item["magazine_number_link"] = "public-view-Test_Magazine_Number_Link"
        test_pipeline = BcuMagazineNumbersPipeline()

        with pytest.raises(DropItem) as err:
            test_pipeline.process_item(test_item, test_spider)

        assert (
            str(err.value) == f"MagazineNumberItem {test_item} dropped due to"
            " incorrect magazine_number_link"
        )

    def test_magazine_number_pipeline_drop_item_due_to_missing_magazine_number_text(
        self,
    ):

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineNumberItem()
        test_item["magazine_year_id"] = 1
        test_item["magazine_number_link"] = "Test_Magazine_Number_Link"
        test_pipeline = BcuMagazineNumbersPipeline()

        with pytest.raises(DropItem) as err:
            test_pipeline.process_item(test_item, test_spider)

        assert (
            str(err.value) == f"MagazineNumberItem {test_item} dropped because"
            " magazine_number is missing"
        )


class TestBcuNumberPageContentPipeline:

    def test_magazine_page_content_pipeline_data_written_in_database(
        self, create_db_tables
    ):
        """
        When a BcuSpiderMagazineContentPageItem is processed the attributes of the
        item should be inserted in a database in magazine_number_content table.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineContentPageItem()
        test_item["magazine_number_id"] = 1
        test_item["magazine_content_text"] = "Test_Magazine_Content_Text"
        test_item["magazine_content_page"] = 1
        test_pipeline = BcuNumberPageContentPipeline()
        test_pipeline.path_database = create_db_tables

        test_pipeline.process_item(test_item, test_spider)

        conn = sqlite3.connect(test_pipeline.path_database)
        c = conn.cursor()
        with conn:
            inserted_magazine_number_id = c.execute(
                "SELECT magazine_number_id from magazine_number_content"
            ).fetchone()[0]
            inserted_magazine_content = c.execute(
                "SELECT magazine_content from magazine_number_content"
            ).fetchone()[0]
            inserted_magazine_page = c.execute(
                "SELECT magazine_page from magazine_number_content"
            ).fetchone()[0]
            inserted_id = c.execute("SELECT id from magazine_number_content").fetchone()

        assert inserted_magazine_number_id == test_item["magazine_number_id"]
        assert inserted_magazine_content == test_item["magazine_content_text"]
        assert inserted_magazine_page == test_item["magazine_content_page"]
        assert inserted_id is not None

    def test_magazine_page_content_pipeline_correct_attributes(self, create_db_tables):
        """
        When a BcuSpiderMagazineContentPageItem is processed the returned item
        should have the same attributes as the one processed.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineContentPageItem()
        test_item["magazine_number_id"] = 1
        test_item["magazine_content_text"] = "Test_Magazine_Content_Text"
        test_item["magazine_content_page"] = 1
        test_pipeline = BcuNumberPageContentPipeline()
        test_pipeline.path_database = create_db_tables

        res = test_pipeline.process_item(test_item, test_spider)

        assert res["magazine_number_id"] == test_item["magazine_number_id"]
        assert res["magazine_content_text"] == test_item["magazine_content_text"]
        assert res["magazine_content_page"] == test_item["magazine_content_page"]

    def test_magazine_page_content_pipeline_with_different_item_type(self):
        """
        When an item different than BcuSpiderMagazineContentPageItem is
        processed the returned item should have the same attributes as the one
        processed and no additional one.
        """

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineItem()
        test_item["name"] = "Test_Magazine_Name"
        test_item["magazine_link"] = "Test_Link"
        test_pipeline = BcuNumberPageContentPipeline()

        res = test_pipeline.process_item(test_item, test_spider)

        assert len(res.keys()) == 2
        assert res["name"] == test_item["name"]
        assert res["magazine_link"] == test_item["magazine_link"]

    def test_magazine_number_pipeline_drop_item_due_to_missing_magazine_content_page(
        self,
    ):

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineContentPageItem()
        test_item["magazine_number_id"] = 1
        test_item["magazine_content_text"] = "Test_Magazine_Content_Text"
        test_pipeline = BcuNumberPageContentPipeline()

        with pytest.raises(DropItem) as err:
            test_pipeline.process_item(test_item, test_spider)

        assert (
            str(err.value)
            == f"ContentPageItem {test_item} dropped becuase magazine_number_page"
            " is missing."
        )

    def test_magazine_number_pipeline_drop_item_due_to_missing_magazine_content_text(
        self,
    ):

        test_spider = BCUSpider()
        test_item = BcuSpiderMagazineContentPageItem()
        test_item["magazine_number_id"] = 1
        test_item["magazine_content_page"] = 1
        test_pipeline = BcuNumberPageContentPipeline()

        with pytest.raises(DropItem) as err:
            test_pipeline.process_item(test_item, test_spider)

        assert (
            str(err.value)
            == f"ContentPageItem {test_item} dropped becuase magazine_content_text"
            " is empty."
        )
