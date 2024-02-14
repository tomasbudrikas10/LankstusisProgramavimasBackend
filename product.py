class Product:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def serialize_array(products):
        serialized = []
        for product in products:
            serialized.append(product.serialize())
        return serialized

    def serialize(self):
        return {"id": self.id, "name": self.name}