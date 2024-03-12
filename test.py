import threading
import time
from tests import tests
import requests
from main import app
from reset_and_seed_db import reset_and_seed_db
import os

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
            response = requests.post(test.url, json=test.body)
        elif test.method == "PUT":
            response = requests.put(test.url, json=test.body)
        elif test.method == "DELETE":
            response = requests.delete(test.url)
        print(response.text)
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