import json

x = """{
    "Name": "Jennifer Smith",
    "Contact Number": 7867567898,
    "Email": "jen123@gmail.com",
    "Hobbies":["Reading", "Sketching", "Horse Riding"]
    }"""


def load_config(filename: str) -> object
    try:
        with open(filename, 'r') as f:
            json.loads(f, object_hook=lambda )