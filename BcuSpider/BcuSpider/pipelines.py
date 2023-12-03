# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pathlib import Path
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from BcuSpider.items import (
    BcuSpiderMagazineItem,
    BcuSpiderMagazineYearItem,
    BcuSpiderMagazineNumberItem,
    BcuSpiderMagazineYearWithoutNumbersItem,
    BcuSpiderMagazineContentPageItem,
)
from BcuSpider.itemsloaders_helpers import (
    write_to_database,
    get_id_from_database,
)


class BcuMagazinesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineItem):
            return item

        write_to_database(
            "test.db",
            "magazines",
            adapter.get("name"),
            adapter.get("magazine_link"),
        )

        item["id"] = get_id_from_database("test.db", "magazines", adapter.get("name"))

        return item


class BcuMagazineYearsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineYearItem):
            return item

        write_to_database(
            "test.db",
            "magazine_year",
            adapter.get("magazine_id"),
            adapter.get("year"),
            adapter.get("magazine_year_link"),
        )

        item["id"] = get_id_from_database(
            "test.db",
            "magazine_year",
            adapter.get("magazine_id"),
            adapter.get("year"),
        )

        return item


class BcuMagazineYearsWithoutNumbersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineYearWithoutNumbersItem):
            return item

        # magazine years without numbers that have multiple magazine links
        if adapter.get("magazine_year_number"):
            write_to_database(
                "test.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
                str(adapter.get("magazine_year_number")),
            )

            item["id"] = get_id_from_database(
                "test.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
            )

        # magazine years without numbers that have a single magazine link
        else:
            write_to_database(
                "test.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
                adapter.get("magazine_year_link"),
            )

            item["id"] = get_id_from_database(
                "test.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
            )

        return item


class BcuMagazineNumbersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not isinstance(item, BcuSpiderMagazineNumberItem):
            return item
        if "public-view" in str(adapter.get("magazine_number_link")):
            raise DropItem(
                f"MagazineNumberItem {item} dropped due to incorrect magazine_number_link"
            )
        if not adapter.get("magazine_number_text"):
            raise DropItem(
                f"MagazineNumberItem {item} dropped because magazine_number is missing"
            )
        else:
            write_to_database(
                "test.db",
                "magazine_number",
                adapter.get("magazine_year_id"),
                adapter.get("magazine_number_text"),
                adapter.get("magazine_number_link"),
            )

        item["id"] = get_id_from_database(
            "test.db",
            "magazine_number",
            adapter.get("magazine_year_id"),
            adapter.get("magazine_number_text"),
        )

        return item


class BcuNumberPageContentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineContentPageItem):
            return item

        magazine_content_page = adapter.get("magazine_content_page")
        magazine_content_text = adapter.get("magazine_content_text")

        if not magazine_content_text:
            raise DropItem(
                f"ContentPageItem {item} dropped becuase magazine_number_text is empty."
            )
        if not magazine_content_page:
            raise DropItem(
                f"ContentPageItem {item} dropped becuase magazine_number_page is missing."
            )

        write_to_database(
            "test.db",
            "magazine_number_content",
            adapter.get("magazine_number_id"),
            adapter.get("magazine_content_text"),
            adapter.get("magazine_content_page"),
        )

        return item
