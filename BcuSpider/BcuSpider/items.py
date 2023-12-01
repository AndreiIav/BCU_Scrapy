# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BcuSpiderMagazineItem(scrapy.Item):
    # magazine_name = scrapy.Field()
    # magazine_link = scrapy.Field()

    # # added after insert
    # magazine_id = scrapy.Field()

    # scrapped data
    name = scrapy.Field()
    magazine_link = scrapy.Field()

    # added after insert
    id = scrapy.Field()


class BcuSpiderMagazineYearItem(scrapy.Item):
    # this data is coming from parse()
    # magazine_name = scrapy.Field()
    # magazine_id = scrapy.Field()

    # # added after insert
    # magazine_year_id = scrapy.Field()

    # magazine_year = scrapy.Field()
    # magazine_year_link = scrapy.Field()

    # this data is coming from parse()
    magazine_id = scrapy.Field()

    # scrapped data
    year = scrapy.Field()
    magazine_year_link = scrapy.Field()

    # added after insert
    id = scrapy.Field()


# MagazineYearItem for magazines that don't have separate numbers page
class BcuSpiderMagazineYearWithoutNumbersItem(scrapy.Item):
    # # this data is coming from parse()
    # magazine_name = scrapy.Field()
    # magazine_id = scrapy.Field()

    # # added after insert
    # magazine_year_id = scrapy.Field()
    # magazine_number_id = scrapy.Field()

    # # Anul 1924, Anul 1925
    # magazine_year_name_without_numbers = scrapy.Field()

    # # for years that have multiple magazine links
    # # [('Partea 1', Partea_1_link), ('Partea 2', Partea_2_link)]
    # magazine_year_number = scrapy.Field()

    # # for years that have a single magazine link
    # magazine_year_link = scrapy.Field()

    # this data is coming from parse()
    magazine_id = scrapy.Field()

    # scrapped data
    # Anul 1924, Anul 1925
    magazine_year_name_without_numbers = scrapy.Field()

    # scrapped data
    # for years that have multiple magazine links
    # [('Partea 1', Partea_1_link), ('Partea 2', Partea_2_link)]
    magazine_year_number = scrapy.Field()

    # scrapped data
    # for years that have a single magazine link
    magazine_year_link = scrapy.Field()

    # added after insert
    id = scrapy.Field()


class BcuSpiderMagazineNumberItem(scrapy.Item):
    # this data is coming from parse_magazine_years
    magazine_name = scrapy.Field()
    magazine_id = scrapy.Field()
    magazine_year = scrapy.Field()
    magazine_year_id = scrapy.Field()

    # added after insert
    magazine_number_id = scrapy.Field()

    # scrapped by parse_magazine_numbers or coming from parse_magazine_years()
    # (for years without numbers)
    magazine_number_text = scrapy.Field()
    magazine_number_link = scrapy.Field()


class BcuSpiderMagazineContentPageItem(scrapy.Item):
    # this data is coming from parse_magazine_numbers (for magazines with numbers)
    # or parse_magazine_years (for magazines without numbers)
    magazine_name = scrapy.Field()
    magazine_id = scrapy.Field()
    magazine_year = scrapy.Field()
    magazine_year_id = scrapy.Field()
    magazine_number_text = scrapy.Field()
    magazine_number_id = scrapy.Field()

    magazine_content_page = scrapy.Field()
    magazine_content_text = scrapy.Field()
