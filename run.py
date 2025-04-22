from app import validator
from app.api import app
import sys

if __name__ == "__main__":
    if "--serve" in sys.argv:
        app.run(host="0.0.0.0", port=5000)
    else:
        validator.main()
