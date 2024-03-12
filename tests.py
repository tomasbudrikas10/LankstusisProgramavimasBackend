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
]