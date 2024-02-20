from flask import Flask, request
from product import Product
from category import Category
from choice import Choice
from category_choices import CategoryChoices
from product_category_choices import ProductCategoryChoices
import mysql.connector
cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="mydb")

app = Flask(__name__)

products = [Product(1, "Produktas A"), Product(2, "Produktas B"), Product(3, "Produktas C")]
categories = [Category(1, "Kategorija A"), Category(2, "Kategorija B"), Category(3, "Kategorija C")]
# Kategorijos ID, egzistuojančių pasirinkimų kategorijoje ID sąrašas
category_choices_arr = [CategoryChoices(1, [1, 2]), CategoryChoices(2, [2, 3]), CategoryChoices(3, [1, 3])]
choices = [Choice(1, "Pasirinkimas A"), Choice(2, "Pasirinkimas B"), Choice(3, "Pasirinkimas C")]
# Produkto ID, Kategorijos ID, Produkto tenkinami pasirinkimai iš nurodytos kategorijos
product_categories_choices = [ProductCategoryChoices(1, 1, [1, 2]), ProductCategoryChoices(2, 2, [3]),
                              ProductCategoryChoices(3, 3, [1])]


@app.route("/")
def hello_world():
    cursor = cnx.cursor()
    query = ("INSERT INTO kategorijos"
             "(pavadinimas)"
             "VALUES (%s)")
    try:
        cursor.execute(query, ("kategorija",))
        cnx.commit()
        cursor.close()
        return "Prideta nauja kategorija"
    except Exception as e:
        cursor.close()
        return str(e)


@app.route("/choices/", methods=["GET", "POST"])
def handle_choices_one():
    if request.method == "GET":
        return Choice.serialize_array(choices)
    elif request.method == "POST":
        json_data = request.json
        errors = []
        if "name" not in json_data:
            errors.append("Name is required")
        else:
            if type(json_data["name"]) != str:
                errors.append("Name must be a string")
            else:
                if len(json_data["name"].strip()) == 0:
                    errors.append("Name must not be empty")
        if len(errors) == 0:
            highest_id = 0
            for choice in choices:
                if choice.id > highest_id:
                    highest_id = choice.id

            choice = Choice(highest_id + 1, json_data["name"])
            choices.append(choice)
            return choice.serialize()
        else:
            return errors
    else:
        return "Bad method"


@app.route("/choices/<int:choice_id>", methods=["GET", "PUT", "DELETE"])
def handle_choices_two(choice_id):
    if request.method == "GET":
        result = "No choice found"
        for choice in choices:
            if choice.id == choice_id:
                result = choice.serialize()
        return result
    elif request.method == "PUT":
        data = request.json
        errors = []
        choice_by_id = ()
        for choice in choices:
            if choice.id == choice_id:
                choice_by_id = choice
        if choice_by_id == ():
            errors.append("No choice found with provided ID")
        else:
            if "name" in data:
                if type(data["name"]) != str:
                    errors.append("Name must be a string")
                else:
                    if data["name"].strip() == "":
                        errors.append("Name must not be empty")
            else:
                errors.append("No name provided")
        if len(errors) == 0:
            choice_by_id.name = data["name"].strip()
            return choice_by_id.serialize()
        else:
            return errors
    elif request.method == "DELETE":
        for choice in choices:
            if choice.id == choice_id:
                index = choices.index(choice)
                choices.pop(index)
                return "Removed choice successfully"
        return "No choice found with provided ID"
    else:
        return "Bad method"


@app.route("/category_choices", methods=["GET", "POST"])
def handle_category_choices_one():
    if request.method == "GET":
        return CategoryChoices.serialize_array(category_choices_arr)
    elif request.method == "POST":
        data = request.json
        errors = []
        if "category_id" not in data:
            errors.append("No category ID is provided")
        elif type(data["category_id"]) != int:
            errors.append("Category ID must be an integer")
        else:
            exists = False
            for category in categories:
                if category.id == data["category_id"]:
                    exists = True
            if exists:
                alreadyCreated = False
                for category_choices in category_choices_arr:
                    if category_choices.category_id == data["category_id"]:
                        alreadyCreated = True
                if alreadyCreated:
                    errors.append("Category with provided ID already has a choices record")
            else:
                errors.append("Category ID provided does not exist")

        if "choice_ids" not in data:
            errors.append("No choice IDs are provided")
        else:
            if type(data["choice_ids"]) == list:
                if len(data["choice_ids"]) == 0:
                    errors.append("Choice IDs list must not be empty")
                else:
                    allInts = True
                    for choice_id in data["choice_ids"]:
                        if type(choice_id) != int:
                            allInts = False
                    if not allInts:
                        errors.append("Choice IDs must be integers")
            else:
                errors.append("Choice IDs must be provided as a list")

        if len(errors) > 0:
            return errors
        else:
            category_choices = CategoryChoices(data["category_id"], data["choice_ids"])
            category_choices_arr.append(category_choices)
            return category_choices.serialize()


@app.route("/category_choices/<int:category_id>", methods=["GET", "PUT", "DELETE"])
def handle_category_choices_two(category_id):
    if request.method == "GET":
        for category_choices in category_choices_arr:
            if category_choices.category_id == category_id:
                return category_choices.serialize()
        return "No category choices record found with provided category ID"
    elif request.method == "PUT":
        data = request.json
        errors = []
        current_category_choices = ()
        for category_choices in category_choices_arr:
            if category_choices.category_id == category_id:
                current_category_choices = category_choices
        if current_category_choices == ():
            errors.append("No category choices record with provided category ID")
        if "choice_ids" not in data:
            errors.append("No choice IDs are provided")
        else:
            if type(data["choice_ids"]) == list:
                if len(data["choice_ids"]) == 0:
                    errors.append("Choice IDs list must not be empty")
                else:
                    allInts = True
                    for choice_id in data["choice_ids"]:
                        if type(choice_id) != int:
                            allInts = False
                    if not allInts:
                        errors.append("Choice IDs must be integers")
            else:
                errors.append("Choice IDs must be provided as a list")

        if len(errors) > 0:
            return errors
        else:
            current_category_choices.choice_ids = data["choice_ids"]
            return current_category_choices.serialize()
    elif request.method == "DELETE":
        for category_choices in category_choices_arr:
            if category_choices.category_id == category_id:
                index = category_choices_arr.index(category_choices)
                category_choices_arr.pop(index)
                return "Removed category choices record successfully"
        return "No category choices record found with provided category ID"
    else:
        return "Bad method"


app.run(debug=True)
