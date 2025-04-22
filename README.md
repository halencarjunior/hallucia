```text
  _    _           _   _                  _____            
 | |  | |         | | | |                |_   _|     /\    
 | |__| |   __ _  | | | |  _   _    ___    | |      /  \   
 |  __  |  / _` | | | | | | | | |  / __|   | |     / /\ \  
 | |  | | | (_| | | | | | | |_| | | (__   _| |_   / ____ \ 
 |_|  |_|  \__,_| |_| |_|  \__,_|  \___| |_____| /_/    \_\

    HallucIA - AI Package Hallucination Analyzer ```
                                                           

# HallucIA

**HallucIA** is a security tool designed to detect and prevent _Package Hallucination_ — a class of vulnerabilities where AI-generated or human-typed code includes dependencies that don't exist or are malicious typosquats.

---

## 🚀 Installation

```bash
git clone https://github.com/your-org/hallucia.git
cd hallucia
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 CLI Usage

### Scan a single file

```bash
python run.py --file example.py
```

### Recursively scan a directory

```bash
python run.py --path ./app
```

### Only show invalid packages

```bash
python run.py --path ./app --only-invalid
```

### Fail CI on invalid packages

```bash
python run.py --path ./app --strict
```

---

## 🌐 API Usage

### Start the API

```bash
python run.py --serve
```

### Check server status

```bash
curl http://localhost:5000/health
```

### Validate code via POST

```bash
curl -X POST http://localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import requests\nimport fakepackage",
    "lang": "python"
  }'
```

### Validate directory (server-side)

```bash
curl -X POST http://localhost:5000/validate-path \
  -H "Content-Type: application/json" \
  -d '{
    "path": "./app",
    "only_invalid": true
  }'
```

---

## 🛡 Features

- Detects non-existent or hallucinated packages
- Supports both Python and JavaScript ecosystems
- Validates native/built-in modules
- CI-ready with `--strict` mode
- Offers API endpoints for remote usage

---

## 🐳 Docker

```bash
docker build -t hallucia .
docker run -p 5000:5000 hallucia
```

---

## 📁 Project Structure

```
hallucia/
├── app/
│   ├── api.py
│   ├── util.py
│   └── validator.py
├── run.py
├── requirements.txt
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🧪 Roadmap

- SARIF output support
- Threat intelligence integration
- Web-based UI for reports

---

## 📄 License

MIT