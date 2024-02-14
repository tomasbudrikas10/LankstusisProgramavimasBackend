from flask import Flask, request
from product import Product
from category import Category
from choice import Choice
from category_choices import CategoryChoices
from product_category_choices import ProductCategoryChoices

app = Flask(__name__)

products = [Product(1, "Produktas A"), Product(2, "Produktas B"), Product(3, "Produktas C")]
categories = [Category(1, "Kategorija A"), Category(2, "Kategorija B"), Category(3, "Kategorija C")]
# Kategorijos ID, egzistuojančių pasirinkimų kategorijoje ID sąrašas
category_choices = [CategoryChoices(1, [1, 2]), CategoryChoices(2, [2, 3]), CategoryChoices(3, [1, 3])]
choices = [Choice(1, "Pasirinkimas A"), Choice(2, "Pasirinkimas B"), Choice(3, "Pasirinkimas C")]
# Produkto ID, Kategorijos ID, Produkto tenkinami pasirinkimai iš nurodytos kategorijos
product_categories_choices = [ProductCategoryChoices(1, 1, [1, 2]), ProductCategoryChoices(2, 2, [3]),
                              ProductCategoryChoices(3, 3, [1])]


@app.route("/")
def hello_world():
    return f"<p>Hello World!</p>"


@app.route("/choices/", methods=["GET", "POST"])
def handle_choices_one():
    if request.method == "GET":
        return Choice.serialize_array(choices)
    elif request.method == "POST":
        json_data = request.json
        errors = []
        if "name" not in json_data:
            errors.append("Name is required")
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
        result = "No choice found"
        data = request.json
        choice_by_id = ()
        for choice in choices:
            if choice.id == choice_id:
                choice_by_id = choice
        if choice_by_id == ():
            return result
        else:
            if any(key in data for key in ["name"]):
                if "name" in data:
                    choice_by_id.name = data["name"]
                return choice_by_id.serialize()
            else:
                result = "No valid data provided"
            return result
    elif request.method == "DELETE":
        for choice in choices:
            if choice.id == choice_id:
                index = choices.index(choice)
                choices.pop(index)
                return "Removed choice successfully"
        return "No choice found with provided ID"
        pass
    else:
        return "Bad method"


app.run(debug=True)
