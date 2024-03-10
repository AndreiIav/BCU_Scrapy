import pytest
from pathlib import Path

from scripts.utils import get_already_inserted_magazine_name


def test_get_already():
    db_path = Path(r"D:\IT projects\BCU_Scrapy_Scrapper\tests") / "scrapy.db"

    assert get_already_inserted_magazine_name(db_path) == []
