from healer.xml import heal_xml


def test_basic_unclosed_tag():
    xml = "<root><item>1<item></root>"

    result = heal_xml(xml)

    assert result.fixed_xml is not None
    assert "<root>" in result.fixed_xml
