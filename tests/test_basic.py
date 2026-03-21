from healer.xml.parser import tokenize

from healer.xml import heal_xml
from healer.xml.classifier import classify
from healer.xml.errors import ErrorType

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


def test_missing_closing():
    xml = "<root><a><b>"
    errors = classify(xml)

    assert ErrorType.MISSING_CLOSING_TAG in errors
    assert all(isinstance(e, ErrorType) for e in errors)


def test_unexpected_closing():
    xml = "<root></a></root>"
    errors = classify(xml)

    assert ErrorType.UNEXPECTED_CLOSING_TAG in errors


def test_broken_tag():
    xml = "<root<<a>"
    errors = classify(xml)

    assert ErrorType.BROKEN_TAG in errors


def test_errors_use_correct_severity():
    result = heal_xml("<root><a><b>")
    assert any(c.severity == 0.2 for c in result.changes)


def test_healer_integration():
    xml = "<root><a><b>"
    result = heal_xml(xml)

    assert result.fixed_xml
    assert result.confidence < 1.0
    assert len(result.changes) > 0


def test_single_root():
    xml = "<a><b></b></a>"
    result = heal_xml(xml)

    assert result.fixed_xml.startswith("<a>")


def test_multiple_roots():
    xml = "<a></a><b></b>"
    result = heal_xml(xml)

    assert result.fixed_xml.startswith("<root>")


def test_text_only():
    xml = "hello world"
    result = heal_xml(xml)

    assert "<root>" in result.fixed_xml

def test_attributes_preserved():
    xml = '<a id="123" class="x"></a>'
    result = heal_xml(xml)

    assert 'id="123"' in result.fixed_xml
    assert 'class="x"' in result.fixed_xml


def test_namespace_tag():
    xml = '<ns:tag></ns:tag>'
    result = heal_xml(xml)

    assert '<ns:tag>' in result.fixed_xml


def test_broken_with_attrs():
    xml = '<a id="1"><b class="x"></a>'
    result = heal_xml(xml)

    assert result.fixed_xml.count("<a") == result.fixed_xml.count("</a>")


def test_comment():
    xml = "<a><!-- hello --></a>"
    result = heal_xml(xml)

    assert "<!-- hello -->" in result.fixed_xml


def test_cdata():
    xml = "<a><![CDATA[ <b>text</b> ]]></a>"
    result = heal_xml(xml)

    assert "<![CDATA[" in result.fixed_xml


def test_processing_instruction():
    xml = '<?xml-stylesheet type="text/xsl"?><a></a>'
    result = heal_xml(xml)

    tokens = tokenize(xml)
    print(tokens)


    assert "<?xml-stylesheet" in result.fixed_xml


def test_diff_detects_change():
    xml = "<a><b></a>"
    result = heal_xml(xml)

    assert len(result.diff) > 0


def test_diff_tag_change():
    xml = "<a><Name>John</NAme>"
    result = heal_xml(xml)
    assert any(c.type == "tag_change" for c in result.diff)