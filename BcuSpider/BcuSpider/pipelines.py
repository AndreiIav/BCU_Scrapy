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
    IncrementId,
    write_to_database,
    get_id_from_database,
)


class BcuMagazinesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineItem):
            return item
        # p = Path(("downloads/magazines.txt"))
        # with open(p, 'a', encoding='utf_8') as magazines:
        #     to_write = (
        #         "magazine_name: "
        #         + adapter.get('magazine_name')
        #         + " magazine_link: "
        #         + adapter.get('magazine_link')
        #         + "\n"
        #     )
        #     magazines.write(to_write)

        write_to_database(
            "test_empty.db",
            "magazines",
            adapter.get("name"),
            adapter.get("magazine_link"),
        )

        # replace with get magazine_id from db
        # item["magazine_id"] = IncrementId.increment_on_call()
        item["id"] = get_id_from_database(
            "test_empty.db", "magazines", adapter.get("name")
        )

        return item


class BcuMagazineYearsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineYearItem):
            return item
        # p = Path(("downloads/magazineYears.txt"))
        # with open(p, "a", encoding="utf_8") as magazine_years:
        #     to_write = (
        #         "magazine_id: "
        #         + str(adapter.get("magazine_id"))
        #         + " magazine_name: "
        #         + adapter.get("magazine_name")
        #         + " magazine_year: "
        #         + adapter.get("magazine_year")
        #         + " magazine_year_link: "
        #         + adapter.get("magazine_year_link")
        #         + "\n"
        #     )
        #     magazine_years.write(to_write)
        write_to_database(
            "test_empty.db",
            "magazine_year",
            adapter.get("magazine_id"),
            adapter.get("year"),
            adapter.get("magazine_year_link"),
        )

        # replace with get magazine_year_id from db
        # item["magazine_year_id"] = IncrementId.increment_on_call()
        item["id"] = get_id_from_database(
            "test_empty.db",
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
            # magazine_years_path = Path(
            #     "downloads/magazineYears.txt"
            # )  # magazineYearsWithoutNumbers.txt
            # with open(
            #     magazine_years_path, "a", encoding="utf_8"
            # ) as magazine_years_numbers:
            #     to_write = (
            #         "magazine_id: "
            #         + str(adapter.get("magazine_id"))
            #         + " magazine_name: "
            #         + adapter.get("magazine_name")
            #         + " magazine_year_name_without_numbers: "
            #         + adapter.get("magazine_year_name_without_numbers")
            #         + " magazine_year_number: "
            #         + str(adapter.get("magazine_year_number"))
            #         + "\n"
            #     )
            #     magazine_years_numbers.write(to_write)
            write_to_database(
                "test_empty.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
                str(adapter.get("magazine_year_number")),
            )

            # replace with get magazine_year_id from db
            # item["magazine_year_id"] = IncrementId.increment_on_call()
            item["id"] = get_id_from_database(
                "test_empty.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
            )

            # magazine_numbers_year_path = Path("downloads/magazineNumbers.txt")
            # for part, link in adapter.get("magazine_year_number"):
            #     with open(magazine_numbers_year_path, "a", encoding="utf_8") as magazine_numbers_year:
            #         to_write = "magazine_id: " + str(adapter.get("magazine_id")) \
            #                     + " magazine_name: " + adapter.get("magazine_name") \
            #                     + " magazine_year_id: " + str(adapter.get("magazine_year_id")) \
            #                     + " magazine_year: " + adapter.get("magazine_year_name_without_numbers")\
            #                     + " magazine_number: " + part.strip() \
            #                     + " magazine_number_link: " + link \
            #                     + "\n"
            #         magazine_numbers_year.write(to_write)
            # replace with get magazine_number_id from db
            # item["magazine_number_id"] = IncrementId.increment_on_call()

        # magazine years without numbers that have a single magazine link
        else:
            # magazine_years_path = Path("downloads/magazineYears.txt")
            # with open(
            #     magazine_years_path, "a", encoding="utf_8"
            # ) as magazine_years_numbers:
            #     to_write = (
            #         "magazine_id: "
            #         + str(adapter.get("magazine_id"))
            #         + " magazine_name: "
            #         + adapter.get("magazine_name")
            #         + " magazine_year_name_without_numbers: "
            #         + adapter.get("magazine_year_name_without_numbers")
            #         + " magazine_year_link: "
            #         + adapter.get("magazine_year_link")
            #         + "\n"
            #     )
            #     magazine_years_numbers.write(to_write)
            write_to_database(
                "test_empty.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
                adapter.get("magazine_year_link"),
            )

            # replace with get magazine_year_id from db
            # item["magazine_year_id"] = IncrementId.increment_on_call()
            item["id"] = get_id_from_database(
                "test_empty.db",
                "magazine_year",
                adapter.get("magazine_id"),
                adapter.get("magazine_year_name_without_numbers"),
            )

            # magazine_numbers_year_path = Path("downloads/magazineNumbers.txt")
            # with open(magazine_numbers_year_path, "a", encoding="utf_8") as magazine_numbers_year:
            #     to_write = "magazine_id: " + str(adapter.get("magazine_id")) \
            #                 + " magazine_name: " + adapter.get("magazine_name") \
            #                 + " magazine_year_id: " + str(adapter.get("magazine_year_id")) \
            #                 + " magazine_year: " + adapter.get("magazine_year_name_without_numbers")\
            #                 + " magazine_number: " + adapter.get("magazine_year_name_without_numbers") \
            #                 + " magazine_number_link: " + adapter.get("magazine_year_link") \
            #                 + "\n"
            #     magazine_numbers_year.write(to_write)
            # replace with get magazine_number_id from db
            # item["magazine_number_id"] = IncrementId.increment_on_call()

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
            p = Path("downloads/magazineNumbers.txt")
            with open(p, "a", encoding="utf_8") as magazine_numbers:
                to_write = (
                    "magazine_id: "
                    + str(adapter.get("magazine_id"))
                    + " magazine_name: "
                    + adapter.get("magazine_name")
                    + " magazine_year_id: "
                    + str(adapter.get("magazine_year_id"))
                    + " magazine_year: "
                    + adapter.get("magazine_year")
                    + " magazine_number: "
                    + adapter.get("magazine_number_text")
                    + " magazine_number_link: "
                    + adapter.get("magazine_number_link")
                    + "\n"
                )
                magazine_numbers.write(to_write)

        item["magazine_number_id"] = IncrementId.increment_on_call()
        return item


class BcuNumberPageContentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not isinstance(item, BcuSpiderMagazineContentPageItem):
            return item

        magazine_name = adapter.get("magazine_name")
        magazine_year = (
            adapter.get("magazine_year").replace('/', '-').replace('\\', '-')
        )
        magazine_number_text = adapter.get("magazine_number_text")
        magazine_number_id = str(adapter.get("magazine_number_id"))

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

        p = (
            Path("downloads/content")
            / f"{magazine_name}_{magazine_year}_{magazine_number_text}_{magazine_number_id}.txt"
        )
        with open(p, "a", encoding="utf_8") as page_content:
            to_write = (
                "page "
                + str(magazine_content_page)
                + "\n"
                + magazine_content_text
                + "\n"
            )
            page_content.write(to_write)

        return item
