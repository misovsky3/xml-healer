from healer.xml import heal_xml


def test_unclosed_tag():
    xml = "<root><a><b></a>"
    result = heal_xml(xml)

    assert "<root>" in result.fixed_xml
    assert result.fixed_xml.count("<a>") == result.fixed_xml.count("</a>")


def test_missing_closing_root():
    xml = "<root><a>text"
    out = heal_xml(xml)

    assert out.fixed_xml.count("<root>") == out.fixed_xml.count("</root>")


def test_nested_break():
    xml = "<a><b><c></a></c>"
    out = heal_xml(xml)

    # no orphan closing tags
    assert out.fixed_xml.count("<a>") == out.fixed_xml.count("</a>")


def test_plain_text_noise():
    xml = "random text <a>hello</b> more text"
    out = heal_xml(xml)

    assert "<a>" in out.fixed_xml


def test_empty_input():
    assert heal_xml("").fixed_xml == ""


def test_result_structure():
    xml = "<root><a><b></a>"
    result = heal_xml(xml)

    assert hasattr(result, "fixed_xml")
    assert hasattr(result, "confidence")
    assert result.fixed_xml
    assert 0 <= result.confidence <= 1


def test_healing_changes():
    xml = "<a><b><c></a>"
    result = heal_xml(xml)

    assert isinstance(result.changes, list)
