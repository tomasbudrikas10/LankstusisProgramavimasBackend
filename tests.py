class Test:
    def __init__(self, name, url, method, expected_status, expected_result, body=None):
        self.name = name
        self.url = "http://127.0.0.1:5000" + url
        self.method = method
        self.expected_status = expected_status
        self.expected_result = expected_result
        self.body = body


tests = [
    Test("Get Products", "/products/", "GET", 200, {
        "message": "Successfully retrieved all products.",
        "data": [
            {
                "id": 1,
                "pavadinimas": "Produktas A",
                "aprasymas": "Aprasymas A",
                "paveiksliukas": "Paveiksliukas A",
                "gamintojas": "Gamintojas A",
                "produkto_puslapis": "Produkto Puslapis A"
            },
            {
                "id": 2,
                "pavadinimas": "Produktas B",
                "aprasymas": "Aprasymas B",
                "paveiksliukas": "Paveiksliukas B",
                "gamintojas": "Gamintojas B",
                "produkto_puslapis": "Produkto Puslapis B"
            },
            {
                "id": 3,
                "pavadinimas": "Produktas C",
                "aprasymas": "Aprasymas C",
                "paveiksliukas": "Paveiksliukas C",
                "gamintojas": "Gamintojas C",
                "produkto_puslapis": "Produkto Puslapis C"
            },
            {
                "id": 4,
                "pavadinimas": "Produktas D",
                "aprasymas": "Aprasymas D",
                "paveiksliukas": "Paveiksliukas D",
                "gamintojas": "Gamintojas D",
                "produkto_puslapis": "Produkto Puslapis D"
            },
            {
                "id": 5,
                "pavadinimas": "Produktas E",
                "aprasymas": "Aprasymas E",
                "paveiksliukas": "Paveiksliukas E",
                "gamintojas": "Gamintojas E",
                "produkto_puslapis": "Produkto Puslapis E"
            }
        ]
    })
]