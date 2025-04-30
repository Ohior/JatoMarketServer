from itertools import product
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from utils.Constants import FIREBASE_PRODUCT_COLLECTION
from data_model.Product import Product
from database.manage_database import add_data_to_firestore, get_all_documents_from_collection, get_all_documents_product, get_data_from_firestore, update_data_in_firestore
from security.api_manage import get_api_key
from utils.Tools import generateUUid

router = APIRouter(prefix="/products", tags=["Products"])


# @router.post("/", response_model=Product)
# async def create_product(product: Product, api_key: str = Depends(get_api_key)):
#     pid = generateUUid()
#     product = product.update({
#         "product_id": pid,
#     })
#     await add_data_to_firestore(
#         document=product.store_id,
#         data=product.model_dump(),
#         collection=FIREBASE_PRODUCT_COLLECTION
#     )
#     # fake_product_db.append(product)
#     return product


@router.get("/{store_id}", response_model=List[Product])
async def get_products(store_id: str, api_key: str = Depends(get_api_key)):
    return await get_all_documents_product(
        document=store_id,
        collection=FIREBASE_PRODUCT_COLLECTION
    )


@router.get("/{store_id}{product_id}", response_model=Product)
async def get_product(store_id: str, product_id: str, api_key: str = Depends(get_api_key)):
    products = await get_all_documents_product(
        document=store_id,
        collection=FIREBASE_PRODUCT_COLLECTION
    )
    return next((product for product in products if product["product_id"] == product_id), HTTPException(status_code=404, detail="Product not found"))


@router.put("/{store_id}{product_id}", response_model=Product)
async def update_product(store_id: str, product_id: str, updated: Product, api_key: str = Depends(get_api_key)):
    products = await get_all_documents_product(
        document=store_id,
        collection=FIREBASE_PRODUCT_COLLECTION
    )
    product =next((product for product in products if product["product_id"] == product_id), HTTPException(status_code=404, detail="Product not found"))
    products.remove(product)
    products.append(updated)
    await update_data_in_firestore(
        document=store_id,
        data=products,
        collection=FIREBASE_PRODUCT_COLLECTION
    )
    return updated


@router.delete("/{store_id}{product_id}")
async def delete_product(store_id: str, product_id: str,  api_key: str = Depends(get_api_key)):
    try:
        products = await get_all_documents_product(
            document=store_id,
            collection=FIREBASE_PRODUCT_COLLECTION
        )
        product =next((product for product in products if product["product_id"] == product_id), HTTPException(status_code=404, detail="Product not found"))
        p = products.pop(product)
        await update_data_in_firestore(
            document=store_id,
            data=products,
            collection=FIREBASE_PRODUCT_COLLECTION
        )
        return p
    except Exception as e:
        raise HTTPException(status_code=404, detail="Product not found")

