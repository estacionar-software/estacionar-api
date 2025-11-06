class ProductOrService:
    def __init__(self, id, description, title, amount, price, type, created_at):
        self.id = id
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