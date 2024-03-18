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
    }),
    Test("Get Product By ID", "/products/3", "GET", 200, {'message': 'Successfully retrieved product with provided ID.', 'data': {'id': 3, 'pavadinimas': 'Produktas C', 'aprasymas': 'Aprasymas C', 'paveiksliukas': 'Paveiksliukas C', 'gamintojas': 'Gamintojas C', 'produkto_puslapis': 'Produkto Puslapis C'}}),
    Test("Get Product By ID that doesn't exist", "/products/6", "GET", 404, {'message': 'Failed to retrieve product.', 'errors': ['No product with provided ID.']}),
    Test("Add Product To Database", "/products", "POST",  200, {'message': 'Successfully created product.'}, {'name':"Produktas F", 'description':"Produktas F", 'image_url': "Paveiksliukas F", 'manufacturer': 'Gamintojas F', 'product_url': 'Produkto Puslapis F'}),
    Test("Add Product With Duplicate Name To Database", "/products", "POST", 400, {'message': 'Failed to create product.', 'errors': ['A product with the provided name already exists']}, {'name': "Produktas F", 'description': "Produktas F", 'image_url': "Paveiksliukas F", 'manufacturer': 'Gamintojas F', 'product_url': 'Produkto Puslapis F'}),
    Test("Add Product With Missing Fields", "/products", "POST", 400, {'message': 'Failed to create product.', 'errors': ['Name is required', 'Description is required', 'Image URL is required', 'Manufacturer is required', 'Product URL is required']}, {}),
    Test("Add Product With Incorrect Field Types Or Values", "/products", "POST", 400, {'message': 'Failed to create product.', 'errors': ['Name must be a string', 'Description must be a string', 'Image URL must be a string', 'Manufacturer must not be empty', 'Product URL must not be empty']}, {"name": 5, "description": 4, "image_url": 2, "manufacturer": " ", "product_url": " "}),
    Test("Delete Product By ID", "/products/6", "DELETE", 200, {'message': 'Removed product successfully.'}),
    Test("Delete Product By ID that doesn't exist", "/products/6", "DELETE", 404, {'message': 'Failed to delete product.', 'errors': ['No product found with provided ID.']}),
    Test("Delete Product By ID that is depended on", "/products/1", "DELETE", 500,{'message': 'Encountered a database error', 'errors': ['1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`tomasbudrikas10$test`.`atsiliepimai`, CONSTRAINT `fk_atsiliepimai_produktai1` FOREIGN KEY (`produktoId`) REFERENCES `produktai` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION)']}),
    Test("Update Product By ID", "/products/2", "PUT", 200, {'message': 'Successfully updated product.'}, {'name':"Produktas F", 'description':"Produktas F", 'image_url': "Paveiksliukas F", 'manufacturer': 'Gamintojas F', 'product_url': 'Produkto Puslapis F'}),
    Test("Update Product With Duplicate Name", "/products/2", "PUT", 400, {'message': 'Failed to update product.', 'errors': ['A product with the provided name already exists']}, {'name': "Produktas A", 'description': "Produktas F", 'image_url': "Paveiksliukas F", 'manufacturer': 'Gamintojas F', 'product_url': 'Produkto Puslapis F'}),
    Test("Update Product With Missing Fields", "/products/2", "PUT", 400, {'message': 'Failed to update product.', 'errors': ['Name is required', 'Description is required', 'Image URL is required', 'Manufacturer is required', 'Product URL is required']}, {}),
    Test("Update Product With Incorrect Field Types Or Values", "/products/2", "PUT", 400, {'message': 'Failed to update product.', 'errors': ['Name must be a string', 'Description must be a string', 'Image URL must be a string', 'Manufacturer must not be empty', 'Product URL must not be empty']}, {"name": 5, "description": 4, "image_url": 2, "manufacturer": " ", "product_url": " "}),
    Test("Get Categories", "/categories", "GET", 200, {
	"message": "Successfully retrieved all categories.",
	"data": [
		{
			"id": 1,
			"pavadinimas": "Kategorija A"
		},
		{
			"id": 2,
			"pavadinimas": "Kategorija B"
		},
		{
			"id": 3,
			"pavadinimas": "Kategorija C"
		},
		{
			"id": 4,
			"pavadinimas": "Kategorija D"
		},
		{
			"id": 5,
			"pavadinimas": "Kategorija E"
		}
	]
}),
    Test("Create Category With Missing Name", "/categories", "POST", 400, {'message': 'Failed to create category.', 'errors': ['Name is required']}, {"nam": "kategorija"}),
    Test("Create Category With Invalid Name Data Type", "/categories", "POST", 400,
         {'message': 'Failed to create category.', 'errors': ['Name must be a string']}, {"name": 5}),
    Test("Create Category With Empty Name", "/categories", "POST", 400,
         {'message': 'Failed to create category.', 'errors': ['Name must not be empty']}, {"name": ""}),
    Test("Create Category With Existing Name", "/categories", "POST", 400, {'message': 'Failed to create category.', 'errors': ['A category with the provided name already exists']}, {"name": "Kategorija A"}),
    Test("Create Category With Valid Data", "/categories", "POST", 200, {'message': 'Successfully created category.'}, {"name": "Kategorija F"}),
    Test("Get Category With Invalid ID", "/categories/7", "GET", 404, {'message': 'Failed to retrieve category.', 'errors': ['No category with provided ID.']}),
    Test("Get Category With Valid ID", "/categories/6", "GET", 200, {'message': 'Successfully retrieved category with provided ID.', 'data': {'id': 6, 'pavadinimas': 'Kategorija F'}}),
    Test("Update Category With Invalid ID", "/categories/7", "PUT", 404, {'message': 'Failed to update category.', 'errors': ['No category with provided ID.']}, {}),
    Test("Update Category With Invalid Data", "/categories/6", "PUT", 400, {'message': 'Failed to update category.', 'errors': ['No name provided']}, {"named": "abc"}),
    Test("Update Category With Existing Name", "/categories/6", "PUT", 400, {'message': 'Failed to update category.', 'errors': ['A category with the provided name already exists']}, {"name": "Kategorija A"}),
    Test("Update Category With Valid Data", "/categories/6", "PUT", 200, {'message': 'Successfully updated category.'}, {"name": "Kategorija G"}),
    Test("Delete Category With Invalid ID", "/categories/8", "DELETE", 404, {'message': 'Failed to remove category.', 'errors': ['No category with provided ID.']}),
    Test("Delete Category With Existing ID", "/categories/6", "DELETE", 200, {'message': 'Removed category successfully.'}),
    Test("Get All Category Choices", "/category_choices", "GET", 200, {'message': 'Successfully retrieved all categories and their choices.', 'data': [{'id': 1, 'kategorijosId': 1, 'pasirinkimoId': 1}, {'id': 2, 'kategorijosId': 1, 'pasirinkimoId': 2}, {'id': 3, 'kategorijosId': 2, 'pasirinkimoId': 3}, {'id': 4, 'kategorijosId': 2, 'pasirinkimoId': 4}, {'id': 5, 'kategorijosId': 3, 'pasirinkimoId': 5}, {'id': 6, 'kategorijosId': 3, 'pasirinkimoId': 1}, {'id': 7, 'kategorijosId': 4, 'pasirinkimoId': 2}, {'id': 8, 'kategorijosId': 4, 'pasirinkimoId': 3}, {'id': 9, 'kategorijosId': 5, 'pasirinkimoId': 4}, {'id': 10, 'kategorijosId': 5, 'pasirinkimoId': 5}]}),
    Test("Add Choice To Category With Invalid Choice ID", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['Choice ID provided must be an integer']}, {"choice_id": "5", "category_id": 1}),
    Test("Add Choice To Category With Missing Choice ID", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['No choice ID is provided']}, {"category_id": 1}),
    Test("Add Choice To Category With Invalid Category ID", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['Category ID must be an integer']}, {"choice_id": 1, "category_id": "5"}),
    Test("Add Choice To Category With Missing Category ID", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['No category ID is provided']}, {"choice_id": 1}),
    Test("Add Choice To Category With Non-Existing Category", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['Category with provided ID does not exist']}, {"category_id":8, "choice_id": 1}),
    Test("Add Choice To Category With Non-Existing Choice", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['Choice with provided ID does not exist']}, {"category_id": 1, "choice_id": 8}),
    Test("Add Choice To Category That Already Has That Choice", "/category_choices", "POST", 400, {'message': 'Failed to add choice to category.', 'errors': ['Category already has this choice']}, {"choice_id":1, "category_id":1}),
    Test("Add Choice To Category With Valid Data", "/category_choices", "POST", 200, {'message': 'Successfully added choice to category.'}, {"choice_id":1, "category_id": 5}),
    Test("Get Category Choices With Valid ID", "/category_choices/1", "GET", 200, {'message': 'Successfully retrieved category and its choices.', 'data': [{'id': 1, 'kategorijosId': 1, 'pasirinkimoId': 1}, {'id': 2, 'kategorijosId': 1, 'pasirinkimoId': 2}]}),
    Test("Get Category Choices With Invalid ID", "/category_choices/6", "GET", 404, {'message': 'Failed to retrieve category and its choices.', 'errors': ['No category choices with provided category ID.']}),
    Test("Delete Category Choices With Valid ID", "/category_choices/1", "DELETE", 200, {'message': 'Successfully deleted all choices for category with provided ID.'}),
    Test("Delete Category Choices With Invalid ID", "/category_choices/1", "DELETE", 404,{'message': 'Failed to delete choices for category.', 'errors': ['Category with provided ID has no choices.']}),
    Test("Update Category Choice With Invalid Choice ID", "/category_choices/3/1", "PUT", 400, {'message': 'Failed to update choices of category.', 'errors': ['Choice ID must be an integer']}, {"choice_id": "5"}),
    Test("Update Category Choice With Missing Choice ID", "/category_choices/3/1", "PUT", 400, {'message': 'Failed to update choices of category.', 'errors': ['No new choice ID provided']}, {"choce_id": 1}),
    Test("Update Category Choice With Non-Existing Choice", "/category_choices/3/1", "PUT", 400, {'message': 'Failed to update choices of category.', 'errors': ['New choice with provided ID does not exist.']}, {"choice_id": 12}),
    Test("Update Category Choice With Already Existing Choice On Category", "/category_choices/3/1", "PUT", 400, {'message': 'Failed to update choices of category.', 'errors': ["Can't change choice ID of this record to one that already exists on this category"]}, {"choice_id": 5}),
    Test("Update Non-Existing Category Choice", "/category_choices/1/1", "PUT", 400, {'message': 'Failed to update choices of category.', 'errors': ['Provided choice for provided category does not exist.']}, {"choice_id": 2}),
    Test("Update Category Choice With Valid Choice", "/category_choices/3/1", "PUT", 200, {'message': 'Successfully updated old choice ID with new choice ID.'}, {"choice_id": 4}),
    Test("Delete Category Choice With Valid Choice", "/category_choices/3/4", "DELETE", 200, {'message': 'Successfully deleted choice on category.'}),
    Test("Delete Category Choice With Invalid Choice", "/category_choices/3/4", "DELETE", 404, {'message': 'Failed to delete choice on category.', 'errors': ['No choice with provided ID on category with provided ID.']})
]