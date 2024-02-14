class ProductCategoryChoices:
    def __init__(self, product_id, category_id, choice_ids):
        self.product_id = product_id
        self.category_id = category_id
        self.choice_ids = choice_ids

    @staticmethod
    def serialize_array(product_category_choices_arr):
        serialized = []
        for product_category_choices in product_category_choices_arr:
            serialized.append(product_category_choices.serialize())
        return serialized

    def serialize(self):
        return {"product_id": self.product_id, "category_id": self.category_id, "choice_ids": self.choice_ids}