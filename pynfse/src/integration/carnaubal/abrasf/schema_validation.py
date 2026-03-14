from functools import lru_cache
from pathlib import Path
from typing import Union

from lxml import etree


SCHEMA_DIR = Path(__file__).resolve().parent / "schema"


@lru_cache(maxsize=None)
def load_schema(schema_filename: str) -> etree.XMLSchema:
    schema_path = SCHEMA_DIR / schema_filename
    schema_doc = etree.parse(str(schema_path))
    return etree.XMLSchema(schema_doc)


def validate_xml(xml_content: Union[str, bytes], schema_filename: str) -> None:
    if isinstance(xml_content, str):
        xml_content = xml_content.encode("utf-8")
    doc = etree.fromstring(xml_content)
    schema = load_schema(schema_filename)
    schema.assertValid(doc)
