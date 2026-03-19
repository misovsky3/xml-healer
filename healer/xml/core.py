from dataclasses import dataclass
from typing import List, Dict, Any

from lxml import etree


@dataclass
class HealResult:
    fixed_xml: str
    changes: List[Dict[str, Any]]


def heal_xml(xml_string: str) -> HealResult:
    changes = []

    # 1. Encoding fix (basic heuristic)
    xml_string, encoding_changes = _fix_encoding(xml_string)
    changes.extend(encoding_changes)

    # 2. Parse with recovery mode
    parser = etree.XMLParser(recover=True)
    try:
        root = etree.fromstring(xml_string.encode("utf-8"), parser=parser)
    except Exception as e:
        return HealResult(
            fixed_xml="",
            changes=[{"type": "fatal_error", "detail": str(e)}]
        )

    # 3. Serialize back
    fixed_xml = etree.tostring(root, encoding="unicode")

    return HealResult(
        fixed_xml=fixed_xml,
        changes=changes
    )


def _fix_encoding(xml_string: str):
    """
    Tries to normalize encoding issues.
    """
    changes = []

    if isinstance(xml_string, bytes):
        try:
            xml_string = xml_string.decode("utf-8")
            changes.append({"type": "encoding_fix", "detail": "decoded utf-8"})
        except UnicodeDecodeError:
            xml_string = xml_string.decode("latin-1")
            changes.append({"type": "encoding_fix", "detail": "decoded latin-1 fallback"})

    # remove BOM if present
    if xml_string.startswith("\ufeff"):
        xml_string = xml_string.replace("\ufeff", "")
        changes.append({"type": "encoding_fix", "detail": "removed BOM"})

    return xml_string, changes
