from flask import Flask, request
import json
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
        try:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pasirinkimai")
            rows = cursor.fetchall()
            cursor.close()
            return json.dumps(rows)
        except Exception as e:
            return str(e)
    elif request.method == "POST":
        query = ("INSERT INTO pasirinkimai"
                 "(pavadinimas)"
                 "VALUES (%s)")
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
            try:
                cursor = cnx.cursor()
                cursor.execute(query, (json_data["name"],))
                cnx.commit()
                cursor.close()
                return json.dumps(json_data)
            except Exception as e:
                return str(e)
        else:
            return errors
    else:
        return "Bad method"


@app.route("/choices/<int:choice_id>", methods=["GET", "PUT", "DELETE"])
def handle_choices_two(choice_id):
    if request.method == "GET":
        try:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM pasirinkimai WHERE id = %s", (choice_id,))
            result = cursor.fetchone()
            if result is not None:
                return json.dumps(result)
            else:
                return "No choice found."
        except Exception as e:
            return str(e)
    elif request.method == "PUT":
        data = request.json
        errors = []
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasirinkimai WHERE id = %s", (choice_id,))
        result = cursor.fetchone()
        if result is None:
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
            cursor.execute("UPDATE `pasirinkimai` SET `pavadinimas`=%s WHERE `id` = %s", (data["name"].strip(), choice_id))
            cnx.commit()
            result["pavadinimas"] = data["name"].strip()
            return json.dumps(result)
        else:
            return errors
    elif request.method == "DELETE":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM pasirinkimai WHERE id = %s", (choice_id,))
        cnx.commit()
        if cursor.rowcount == 0:
            return "No choice found with provided ID"
        else:
            return "Removed choice successfully"
    else:
        return "Bad method"


@app.route("/category_choices", methods=["GET", "POST"])
def handle_category_choices_one():
    if request.method == "GET":
        try:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM kategorijospasirinkimai")
            result = cursor.fetchall()
            return json.dumps(result)
        except Exception as e:
            return str(e)
    elif request.method == "POST":
        data = request.json
        errors = []
        cursor = cnx.cursor()
        if "category_id" not in data:
            errors.append("No category ID is provided")
        elif type(data["category_id"]) != int:
            errors.append("Category ID must be an integer")
        else:
            cursor.execute("SELECT * FROM kategorijos WHERE id = %s", (data["category_id"],))
            result = cursor.fetchone()
            if result is None:
                errors.append("Category with provided ID does not exist")
        if "choice_id" not in data:
            errors.append("No choice ID is provided")
        elif type(data["choice_id"]) != int:
            errors.append("Choice ID provided must be an integer")
        else:
            cursor.execute("SELECT * FROM pasirinkimai WHERE id = %s", (data["choice_id"],))
            result = cursor.fetchone()
            if result is None:
                errors.append("Choice with provided ID does not exist")
        if len(errors) > 0:
            return errors
        else:
            cursor.execute("SELECT * FROM kategorijospasirinkimai where (kategorijosId = %s AND pasirinkimoId = %s)", (data["category_id"], data["choice_id"]))
            result = cursor.fetchone()
            if result is not None:
                errors.append("Category already has this choice")
                cursor.close()
                return errors
            else:
                try:
                    cursor.execute("INSERT INTO kategorijospasirinkimai (kategorijosId, pasirinkimoId) VALUES (%s, %s)", (data["category_id"], data["choice_id"]))
                    cnx.commit()
                    cursor.close()
                    return "Successfully added choice to category"
                except Exception as e:
                    cursor.close()
                    return str(e)


@app.route("/category_choices/<int:category_id>", methods=["GET", "DELETE"])
def handle_category_choices_two(category_id):
    if request.method == "GET":
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kategorijospasirinkimai WHERE kategorijosId = %s", (category_id,))
        result = cursor.fetchall()
        cursor.close()
        if cursor.rowcount == 0:
            return "No category choices found with provided category ID"
        else:
            return json.dumps(result)
    elif request.method == "DELETE":
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("DELETE FROM kategorijospasirinkimai WHERE kategorijosId = %s", (category_id,))
        cnx.commit()
        cursor.close()
        if cursor.rowcount > 0:
            return "Successfully deleted all rows with provided category ID: " + str(cursor.rowcount) + " rows affected."
        else:
            return "No category choices records found with provided category ID"
    else:
        return "Bad method"


@app.route("/category_choices/<int:category_id>/<int:choice_id>", methods=["PUT", "DELETE"])
def handle_category_choices_three(category_id, choice_id):
    if request.method == "PUT":
        json_data = request.json
        errs = []
        cursor = cnx.cursor(dictionary=True)
        if "choice_id" not in json_data:
            errs.append("No new choice ID provided")
        elif type(json_data["choice_id"]) != int:
            errs.append("Choice ID must be an integer")
        else:
            cursor.execute("SELECT * FROM pasirinkimai WHERE id = %s", (json_data["choice_id"],))
            result = cursor.fetchone()
            if result is not None:
                cursor.execute("SELECT * FROM kategorijospasirinkimai WHERE (kategorijosId = %s AND pasirinkimoId = %s)", (category_id, json_data["choice_id"]))
                result2 = cursor.fetchone()
                if result2 is not None:
                    errs.append("Can't change choice ID of this record to one that already exists on this category")
        if len(errs) > 0:
            cursor.close()
            return errs
        else:
            try:
                cursor.execute(
                    "UPDATE kategorijospasirinkimai SET pasirinkimoId = %s WHERE (kategorijosId = %s AND pasirinkimoId = %s)",
                    (json_data["choice_id"], category_id, choice_id))
                cnx.commit()
                cursor.close()
                return "Successfully updated choice ID"
            except Exception as e:
                cursor.close()
                return str(e)
    elif request.method == "DELETE":
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("DELETE FROM kategorijospasirinkimai WHERE (kategorijosId = %s AND pasirinkimoId = %s)", (category_id, choice_id))
        cnx.commit()
        cursor.close()
        if cursor.rowcount > 0:
            return "Successfully deleted choice on category."
        else:
            return "No choice with provided ID on category with provided ID found."
    else:
        return "Bad method"


app.run(debug=True)
