import argparse
from healer.xml import heal_xml

def main():
    print("[DEBUG] CLI main() called")
    parser = argparse.ArgumentParser(description="XML Healer CLI")
    parser.add_argument(
        "input",
        help="XML string or file path"
    )
    parser.add_argument(
        "--file",
        action="store_true",
        help="Treat input as file path"
    )
    args = parser.parse_args()
    print(f"[DEBUG] args: {args}")
    if args.file:
        with open(args.input, "r", encoding="utf-8") as f:
            xml = f.read()
    else:
        xml = args.input
    result = heal_xml(xml)
    print("\n--- FIXED XML ---\n")
    print(result.fixed_xml)
    print("\n--- CONFIDENCE ---\n")
    print(result.confidence)
    print("\n--- CHANGES ---\n")
    for c in result.diff:
        print(c)

if __name__ == "__main__":
    main()
