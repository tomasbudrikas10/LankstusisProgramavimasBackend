class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def serialize_array(categories):
        serialized = []
        for category in categories:
            category.append(category.serialize())
        return serialized

    def serialize(self):
        return {"id": self.id, "name": self.name}