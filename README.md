# xml-healer

A Python tool for healing and diffing broken XML. Automatically fixes common XML errors and provides a diff of changes.

## Features
- Repairs broken or malformed XML
- Detects and reports tag mismatches, missing/extra tags, and text changes
- Provides a diff of all structural and tag changes
- Easy to use API and CLI

## Usage (Python)
```python
from healer.xml import heal_xml

xml = "<a><Name>John</NAme>"
result = heal_xml(xml)
print(result.fixed_xml)
print(result.diff)
```

## Usage (Command Line)
You can use the CLI after installing:

```sh
xml-healer '<a><Name>John</NAme>'
```

Or to heal an XML file:

```sh
xml-healer path/to/file.xml --file
```

**If you have issues with the CLI script (especially on Windows or in a virtual environment), use:**

```sh
python -m healer.cli '<a><Name>John</NAme>'
```

This always works as long as your environment can import the `healer` package.

## Troubleshooting CLI
- Always activate your virtual environment before installing or running the CLI.
- If `xml-healer` is not found, use `.venv\Scripts\xml-healer.exe ...` or `python -m healer.cli ...`.
- If you see `ModuleNotFoundError: No module named 'healer'`, you are running the CLI from a Python environment that cannot see your package. Activate your venv or reinstall in the correct environment.
- For global CLI, install from PyPI in a clean environment.

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
