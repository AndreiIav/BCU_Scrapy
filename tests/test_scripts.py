import pytest
from pathlib import Path

from scripts.utils import get_already_inserted_magazine_name
from scripts.scripts_config import DATABASE_NAME


def test_get_already(config):
    db_path = Path(r"D:\IT projects\BCU_Scrapy_Scrapper\tests") / DATABASE_NAME

    assert get_already_inserted_magazine_name(db_path) == []
