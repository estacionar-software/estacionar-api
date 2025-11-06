def create_product_or_service(id = int, description = str, title = str, amount = int, price = int, type = str):
    print("id:", id)
    print("description: ", description)
    print("title: ", title)
    print("amount: ", amount)
    print("price: ", price)
    print("type: ", type)

    return {"message":"sucesso!"}, 200