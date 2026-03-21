# xml-healer

A Python tool for healing and diffing broken XML. Automatically fixes common XML errors and provides a diff of changes.

## Features
- Repairs broken or malformed XML
- Detects and reports tag mismatches, missing/extra tags, and text changes
- Provides a diff of all structural and tag changes
- Easy to use API

## Usage
```python
from healer.xml import heal_xml

xml = "<a><Name>John</NAme>"
result = heal_xml(xml)
print(result.fixed_xml)
print(result.diff)
```

## Installation
```sh
pip install xml-healer
```

## Testing
Run all tests with:
```sh
pytest
```

## License
MIT
