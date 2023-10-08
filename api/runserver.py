import os

os.system("poetry run python -m uvicorn api.src.app:app --reload --port 8001")