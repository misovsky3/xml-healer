from .fixes import fix_unclosed_tags


def heal_xml(xml: str) -> str:
    """
    Very first version of XML healer.
    Fixes basic structural issues.
    """

    if not isinstance(xml, str):
        raise TypeError("XML must be string")

    xml = xml.strip()

    # 1. basic cleanup
    xml = xml.replace("\n", " ").replace("\t", " ")

    # 2. fix unclosed tags
    xml = fix_unclosed_tags(xml)

    return xml
