import os

os.system("poetry run python -m uvicorn src.app:app --reload --port 8001")