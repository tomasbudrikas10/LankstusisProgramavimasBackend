from flask import Flask, request
import json
import mysql.connector
cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="mydb")

app = Flask(__name__)


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


@app.route("/products/", methods=["GET", "POST"])
def handle_products_one():
    if request.method == "GET":
        try:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM produktai")
            rows = cursor.fetchall()
            cursor.close()
            return json.dumps(rows)
        except Exception as e:
            return str(e)
    elif request.method == "POST":
        query = ("INSERT INTO produktai"
                 "(pavadinimas, aprasymas, paveiksliukas, gamintojas, produkto_puslapis)"
                 "VALUES (%s, %s, %s, %s, %s)")
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
                else:
                    try:
                        cursor = cnx.cursor(dictionary=True)
                        cursor.execute("SELECT * FROM produktai WHERE `pavadinimas`=%s", (json_data["name"],))
                        result = cursor.fetchone()
                        cursor.close()
                        if result is not None:
                            errors.append("A product with the provided name already exists")
                    except Exception as e:
                        return str(e)
        if "description" not in json_data:
            errors.append("Description is required")
        else:
            if type(json_data["description"]) != str:
                errors.append("Description must be a string")
            else:
                if len(json_data["description"].strip()) == 0:
                    errors.append("Description must not be empty")
        if "image_url" not in json_data:
            errors.append("Image URL is required")
        else:
            if type(json_data["image_url"]) != str:
                errors.append("Image URL must be a string")
            else:
                if len(json_data["image_url"].strip()) == 0:
                    errors.append("Image URL must not be empty")
        if "manufacturer" not in json_data:
            errors.append("Manufacturer is required")
        else:
            if type(json_data["manufacturer"]) != str:
                errors.append("Manufacturer must be a string")
            else:
                if len(json_data["manufacturer"].strip()) == 0:
                    errors.append("Manufacturer must not be empty")
        if "product_url" not in json_data:
            errors.append("Product URL is required")
        else:
            if type(json_data["product_url"]) != str:
                errors.append("Product URL must be a string")
            else:
                if len(json_data["product_url"].strip()) == 0:
                    errors.append("Product URL must not be empty")
        if len(errors) == 0:
            try:
                cursor = cnx.cursor()
                cursor.execute(query, (json_data["name"].strip(), json_data["description"].strip(), json_data["image_url"].strip(), json_data["manufacturer"].strip(), json_data["product_url"].strip()))
                cnx.commit()
                cursor.close()
                return "Successfully created product."
            except Exception as e:
                return str(e)
        else:
            return errors
    else:
        return "Bad method"


@app.route("/products/<int:product_id>", methods=["GET", "PUT", "DELETE"])
def handle_products_two(product_id):
    if request.method == "GET":
        try:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM produktai WHERE id = %s", (product_id,))
            cursor.close()
            result = cursor.fetchone()
            if result is not None:
                return json.dumps(result)
            else:
                return "No product found."
        except Exception as e:
            return str(e)
    elif request.method == "PUT":
        json_data = request.json
        errors = []
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produktai WHERE id = %s", (product_id,))
        result = cursor.fetchone()
        if result is None:
            errors.append("No product found with provided ID")
        else:
            if "name" not in json_data:
                errors.append("Name is required")
            else:
                if type(json_data["name"]) != str:
                    errors.append("Name must be a string")
                else:
                    if len(json_data["name"].strip()) == 0:
                        errors.append("Name must not be empty")
                    else:
                        try:
                            cursor.execute("SELECT * FROM produktai WHERE `pavadinimas`=%s", (json_data["name"],))
                            result = cursor.fetchone()
                            if result is not None and result["id"] != product_id:
                                errors.append("A product with the provided name already exists")
                        except Exception as e:
                            cursor.close()
                            return str(e)
            if "description" not in json_data:
                errors.append("Description is required")
            else:
                if type(json_data["description"]) != str:
                    errors.append("Description must be a string")
                else:
                    if len(json_data["description"].strip()) == 0:
                        errors.append("Description must not be empty")
            if "image_url" not in json_data:
                errors.append("Image URL is required")
            else:
                if type(json_data["image_url"]) != str:
                    errors.append("Image URL must be a string")
                else:
                    if len(json_data["image_url"].strip()) == 0:
                        errors.append("Image URL must not be empty")
            if "manufacturer" not in json_data:
                errors.append("Manufacturer is required")
            else:
                if type(json_data["manufacturer"]) != str:
                    errors.append("Manufacturer must be a string")
                else:
                    if len(json_data["manufacturer"].strip()) == 0:
                        errors.append("Manufacturer must not be empty")
            if "product_url" not in json_data:
                errors.append("Product URL is required")
            else:
                if type(json_data["product_url"]) != str:
                    errors.append("Product URL must be a string")
                else:
                    if len(json_data["product_url"].strip()) == 0:
                        errors.append("Product URL must not be empty")
        if len(errors) == 0:
            try:
                cursor.execute("UPDATE `produktai` SET `pavadinimas`=%s, `aprasymas`=%s, `paveiksliukas`=%s, `gamintojas`=%s, `produkto_puslapis`=%s WHERE `id` = %s", (json_data["name"].strip(), json_data["description"].strip(), json_data["image_url"].strip(), json_data["manufacturer"].strip(), json_data["product_url"].strip(), product_id))
                cursor.close()
                cnx.commit()
                return "Successfully updated product."
            except Exception as e:
                cursor.close()
                return str(e)
        else:
            cursor.close()
            return errors
    elif request.method == "DELETE":
        try:
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM produktai WHERE id = %s", (product_id,))
            cursor.close()
            cnx.commit()
            if cursor.rowcount == 0:
                return "No product found with provided ID"
            else:
                return "Removed product successfully"
        except Exception as e:
            return str(e)
    else:
        return "Bad method"


@app.route("/categories/", methods=["GET", "POST"])
def handle_categories_one():
    if request.method == "GET":
        try:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM kategorijos")
            rows = cursor.fetchall()
            cursor.close()
            return json.dumps(rows)
        except Exception as e:
            return str(e)
    elif request.method == "POST":
        query = ("INSERT INTO kategorijos"
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


@app.route("/categories/<int:category_id>", methods=["GET", "PUT", "DELETE"])
def handle_categories_two(category_id):
    if request.method == "GET":
        try:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM kategorijos WHERE id = %s", (category_id,))
            result = cursor.fetchone()
            if result is not None:
                return json.dumps(result)
            else:
                return "No category found."
        except Exception as e:
            return str(e)
    elif request.method == "PUT":
        data = request.json
        errors = []
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kategorijos WHERE id = %s", (category_id,))
        result = cursor.fetchone()
        if result is None:
            errors.append("No category found with provided ID")
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
            cursor.execute("UPDATE `kategorijos` SET `pavadinimas`=%s WHERE `id` = %s", (data["name"].strip(), category_id))
            cnx.commit()
            result["pavadinimas"] = data["name"].strip()
            return json.dumps(result)
        else:
            return errors
    elif request.method == "DELETE":
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM kategorijos WHERE id = %s", (category_id,))
        cnx.commit()
        if cursor.rowcount == 0:
            return "No category found with provided ID"
        else:
            return "Removed category successfully"
    else:
        return "Bad method"


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
