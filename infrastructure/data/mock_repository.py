import json
from pathlib import Path

def load_mock_data():
    path = Path(__file__).parent / "mock_data.json"
    with open(path, "r") as file:
        data = json.load(file)
    return data["database"]
