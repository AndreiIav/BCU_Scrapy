from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class BcuMagazineLoader(ItemLoader):
    default_output_processor = TakeFirst()
    magazine_link_in = MapCompose(
        lambda x: "https://documente.bcucluj.ro/" + x.strip(),
        lambda x: x + "/" if x[-1] != "/" else x,
    )


class BcuMagazineYearLoader(ItemLoader):
    default_output_processor = TakeFirst()
    year_in = MapCompose(lambda x: " ".join(x.split()))


class BcuMagazineNumberLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BcuMagazineYearWithoutNumbersLoader(ItemLoader):
    default_output_processor = TakeFirst()
    magazine_year_name_without_numbers_in = MapCompose(lambda x: " ".join(x.split()))


class BcuMagazineContentPageLoader(ItemLoader):
    default_output_processor = TakeFirst()
    magazine_content_text_in = MapCompose(
        lambda x: x.replace(">", "").replace("<", "").replace("  ", " ")
    )
