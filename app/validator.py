import argparse
import sys
import json
import os
from app.util import validate_packages, filter_only_invalid
from app import __version__

def process_directory(path):
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py") or file.endswith(".js"):
                full_path = os.path.join(root, file)
                lang = "python" if file.endswith(".py") else "javascript"
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    result = validate_packages(code, lang)
                    result["file"] = full_path
                    results.append(result)
                except Exception as e:
                    results.append({
                        "file": full_path,
                        "language": lang,
                        "packages": [],
                        "error": str(e)
                    })
    return results

def has_invalid_packages(results):
    for result in results:
        for pkg in result.get("packages", []):
            if pkg["status"] == "invalid":
                return True
    return False

def main():
    print(rf"""
  _    _           _   _                  _____            
 | |  | |         | | | |                |_   _|     /\    
 | |__| |   __ _  | | | |  _   _    ___    | |      /  \   
 |  __  |  / _` | | | | | | | | |  / __|   | |     / /\ \  
 | |  | | | (_| | | | | | | |_| | | (__   _| |_   / ____ \ 
 |_|  |_|  \__,_| |_| |_|  \__,_|  \___| |_____| /_/    \_\
                                                           
    HallucIA - AI Package Hallucination Validator v{__version__}
""")

    parser = argparse.ArgumentParser(description="Validate packages in Python/JS code.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to .py or .js file")
    group.add_argument("--stdin", action="store_true", help="Read code from stdin")
    group.add_argument("--path", help="Path to directory to scan recursively")
    parser.add_argument("--lang", help="Language: python or javascript (required with --stdin)")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if any invalid packages are found")
    parser.add_argument("--output", help="Path to save the full JSON result")
    parser.add_argument("--summary-only", action="store_true", help="Suppress full output, only show summary")
    parser.add_argument("--only-invalid", action="store_true", help="Show only invalid packages in output")
    parser.add_argument("--version", action="store_true", help="Show the current version")

    args = parser.parse_args()

    if args.version:
        print(f"HallucIA v{__version__}")
        sys.exit(0)

    results = []

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
        lang = "python" if args.file.endswith(".py") else "javascript"
        results = [validate_packages(code, lang)]
        results[0]["file"] = args.file

    elif args.stdin:
        if not args.lang:
            print("Error: --lang is required when using --stdin")
            sys.exit(1)
        code = sys.stdin.read()
        results = [validate_packages(code, args.lang)]
        results[0]["file"] = "stdin"

    elif args.path:
        results = process_directory(args.path)

    output_data = filter_only_invalid(results) if args.only_invalid else results

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

    if not args.summary_only:
        print(json.dumps(output_data, indent=2))

    if args.strict and has_invalid_packages(results):
        sys.exit(1)

if __name__ == "__main__":
    main()