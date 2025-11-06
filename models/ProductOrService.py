import uuid
import datetime
class ProductOrService:
    def __init__(self, description, title, amount, price, type, id = None, created_at = None):
        self.id = id or str(uuid.uuid4())
        self.description = description
        self.title = title
        self.amount = amount
        self.price = price
        self.type = type
        self.created_at = created_at or datetime.datetime.now()

    def to_dictionary(self):
        return {
            'id' : self.id,
            'description' : self.description,
            'title' : self.title,
            'amount' : self.amount,
            'price' : self.price,
            'type' : self.type,
            'created_at' : self.created_at.isoformat(),
        }