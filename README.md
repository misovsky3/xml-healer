# XML Healer 🛠️

Auto-healing tool for broken XML data.

## ✨ Features
- Fix encoding issues (latin1 → utf-8)
- Close unclosed tags
- Wrap stray text into valid XML
- Provide detailed change log

## 🚀 Installation
```bash
pip install xml-healer
```

## 🧪 Usage

``` python
from healer import heal_xml

xml = "<root><item>1<item></root>"

result = heal_xml(xml)

print(result.fixed_xml)
print(result.changes)
```

## 📌 Example Output

``` json
{
  "fixed_xml": "<root><item>1</item></root>",
  "changes": [
    "closed unclosed tag <item>"
  ]
}

```
