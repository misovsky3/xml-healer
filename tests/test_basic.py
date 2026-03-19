from healer.xml import heal_xml


def test_basic_unclosed_tag():
    xml = "<root><item>1<item></root>"

    fixed = heal_xml(xml)

    assert fixed is not None
    assert "<root>" in fixed

def test_basic_heal():
    broken = "<root><a><b></a>"
    fixed = heal_xml(broken)

    assert "<root>" in fixed
    assert fixed.count("<a>") == fixed.count("</a>")
