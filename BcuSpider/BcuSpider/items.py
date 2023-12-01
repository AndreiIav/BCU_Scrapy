# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BcuSpiderMagazineItem(scrapy.Item):
    # scrapped data
    name = scrapy.Field()
    magazine_link = scrapy.Field()

    # added after insert in db
    id = scrapy.Field()


class BcuSpiderMagazineYearItem(scrapy.Item):
    # this data is coming from parse()
    magazine_id = scrapy.Field()

    # scrapped data
    year = scrapy.Field()
    magazine_year_link = scrapy.Field()

    # added after insert in db
    id = scrapy.Field()


class BcuSpiderMagazineYearWithoutNumbersItem(scrapy.Item):
    """
    MagazineYearItem for magazines that don't have separate numbers page.
    """

    # this data is coming from parse()
    magazine_id = scrapy.Field()

    # scrapped data
    # the data looks like this: 'Anul 1924'
    magazine_year_name_without_numbers = scrapy.Field()

    # scrapped data
    # for years that have multiple magazine links
    # the data looks like this: [('Partea 1', Partea_1_link), ('Partea 2', Partea_2_link)]
    magazine_year_number = scrapy.Field()

    # scrapped data
    # for years that have a single magazine link
    magazine_year_link = scrapy.Field()

    # added after insert
    id = scrapy.Field()


class BcuSpiderMagazineNumberItem(scrapy.Item):
    # this data is coming from parse_magazine_years
    magazine_year_id = scrapy.Field()

    # scrapped by parse_magazine_numbers or coming from parse_magazine_years()
    # (for years without numbers)
    magazine_number_text = scrapy.Field()
    magazine_number_link = scrapy.Field()

    # added after insert in db
    id = scrapy.Field()


class BcuSpiderMagazineContentPageItem(scrapy.Item):
    # this data is coming from parse_magazine_numbers (for magazines with numbers)
    # or parse_magazine_years (for magazines without numbers)
    magazine_number_id = scrapy.Field()

    # scrapped data
    magazine_content_page = scrapy.Field()
    magazine_content_text = scrapy.Field()
