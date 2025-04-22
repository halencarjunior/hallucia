# app/util.py

import sys
import importlib.util
import requests
import re

NODE_BUILTINS = {
    "assert", "buffer", "child_process", "cluster", "console", "constants",
    "crypto", "dgram", "dns", "domain", "events", "fs", "http", "http2",
    "https", "inspector", "module", "net", "os", "path", "perf_hooks",
    "process", "punycode", "querystring", "readline", "repl", "stream",
    "string_decoder", "timers", "tls", "trace_events", "tty", "url",
    "util", "v8", "vm", "worker_threads", "zlib"
}

def is_builtin_python_package(package_name):
    return (
        package_name in sys.builtin_module_names or
        importlib.util.find_spec(package_name) is not None
    )

def is_node_builtin(package_name):
    return package_name in NODE_BUILTINS

def check_pypi(package_name):
    if is_builtin_python_package(package_name):
        return True
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    return response.status_code == 200

def check_npm(package_name):
    if is_node_builtin(package_name):
        return True
    url = f"https://registry.npmjs.org/{package_name}"
    response = requests.get(url)
    return response.status_code == 200

def extract_python_packages(code):
    packages = set()
    lines = code.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("import "):
            items = line.replace("import", "").split(",")
            for item in items:
                pkg = item.strip().split('.')[0]
                if pkg:
                    packages.add(pkg)
        elif line.startswith("from "):
            parts = line.split()
            if len(parts) >= 2:
                pkg = parts[1].split('.')[0]
                if pkg:
                    packages.add(pkg)
        elif "pip install" in line:
            match = re.search(r'pip\s+install\s+([a-zA-Z0-9_\-]+)', line)
            if match:
                packages.add(match.group(1))
    return packages

def extract_javascript_packages(code):
    packages = set()
    lines = code.splitlines()
    for line in lines:
        line = line.strip()
        match = re.search(r"require\(['\"]([a-zA-Z0-9_\-]+)['\"]\)", line)
        if match:
            packages.add(match.group(1))
        match = re.search(r"import\s+.*\s+from\s+['\"]([a-zA-Z0-9_\-]+)['\"]", line)
        if match:
            packages.add(match.group(1))
        match = re.search(r"npm\s+install\s+([a-zA-Z0-9_\-]+)", line)
        if match:
            packages.add(match.group(1))
    return packages

def validate_packages(code, lang):
    if lang.lower() == "python":
        packages = extract_python_packages(code)
        checker = check_pypi
    elif lang.lower() in ["js", "javascript"]:
        packages = extract_javascript_packages(code)
        checker = check_npm
    else:
        raise ValueError("Unsupported language. Use 'python' or 'javascript'.")

    results = []
    for pkg in packages:
        try:
            valid = checker(pkg)
            results.append({"name": pkg, "status": "valid" if valid else "invalid"})
        except Exception as e:
            results.append({"name": pkg, "status": "error", "message": str(e)})
    return {
        "language": lang.lower(),
        "packages": results
    }

def filter_only_invalid(results):
    filtered = []
    for result in results:
        invalids = [pkg for pkg in result.get("packages", []) if pkg["status"] == "invalid"]
        if invalids:
            filtered.append({
                "file": result.get("file"),
                "language": result.get("language"),
                "packages": invalids
            })
    return filtered
