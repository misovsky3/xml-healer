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



def test_realistic_xml():
    xml = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <root>
    <osoba id="1">
        <meno>Peter</meno>
        <priezvisko>Hruška</priezvisko>
        <vek>28
    </osoba>

    <osoba id="2">
        <meno>Anna</meno>
        <pozicia><b>Programátorka</pozicia></b>
        <firma meno="Mesto & Les">
    </osoba>

    <osoba id=3,>
        <meno>Lucia</meno>
    </osoba>
    '''
    result = heal_xml(xml)

    assert True