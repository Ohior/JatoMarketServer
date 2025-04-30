import asyncio
from json import dumps, load, loads

from data_model.Product import Product
from database.manage_database import get_all_documents_from_collection
from utils.Tools import generateUUid


# data = asyncio.run(
#     get_all_documents_from_collection(
#         collection="data",
#         # data=Product(
#         #     uid=generateUUid(),
#         #     name="Phone",
#         #     price=200.5,
#         #     quantity=10,
#         # ).model_dump()
#     )
# )

# print(dumps(data, indent=2))