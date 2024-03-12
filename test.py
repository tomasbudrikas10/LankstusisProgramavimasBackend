import threading
import time

import requests
from main import app
from reset_and_seed_db import reset_and_seed_db
import os
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


def run_tests(tests_arg):
    print("Sleeping 3 seconds for Flask app.")
    time.sleep(3)
    print("Running tests: \n")
    for test in tests_arg:
        errs = []
        print("Running test: " + test.name)
        response = None
        if test.method == "GET":
            response = requests.get(test.url)
        elif test.method == "POST":
            response = requests.post(test.url, test.body)
        elif test.method == "PUT":
            response = requests.put(test.url, test.body)
        elif test.method == "DELETE":
            response = requests.delete(test.url)
        if str(response.json()) != str(test.expected_result):
            errs.append("Expected result and actual result do not match.\n" +
                        "Expected result: " + str(test.expected_result)+ "\n" +
                        "Actual result: " + str(response.json()))
        if str(response.status_code) != str(test.expected_status):
            errs.append("Expected status code and actual status code do not match.\n" +
                        "Expected status: " + str(test.expected_status) + "\n" +
                        "Actual status: " + str(response.status_code))
        if len(errs) > 0:
            print("Test failed.")
            print()
            for err in errs:
                print(err)
                print()
        else:
            print("Test passed.")
            print()


if __name__ == "__main__":
    os.environ["mode"] = "test"
    reset_and_seed_db()
    test_thread= threading.Thread(target=run_tests, args=(tests,))
    test_thread.start()
    app.run()
    test_thread.join()
    del os.environ["mode"]