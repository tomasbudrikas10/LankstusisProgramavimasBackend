class CategoryChoices:
    def __init__(self, category_id, choice_ids):
        self.category_id = category_id
        self.choice_ids = choice_ids

    @staticmethod
    def serialize_array(category_choices_arr):
        serialized = []
        for category_choices in category_choices_arr:
            serialized.append(category_choices.serialize())
        return serialized

    def serialize(self):
        return {"category_id": self.category_id, "choice_ids": self.choice_ids}