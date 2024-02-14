class Choice:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def serialize_array(choices):
        serialized = []
        for choice in choices:
            serialized.append(choice.serialize())
        return serialized

    def serialize(self):
        return {"id": self.id, "name": self.name}