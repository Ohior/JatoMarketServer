from fastapi import APIRouter, HTTPException, Depends
from typing import List
from utils.Constants import FIREBASE_PRODUCT_COLLECTION
from data_model.Product import Product
from database.manage_database import add_product_to_firestore, delete_product_from_firestore, get_all_documents_product, get_product_document, update_data_in_firestore, update_product_in_firestore
from security.api_manage import get_api_key
from utils.Tools import generateUUid

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/{store_id}", response_model=Product)
async def create_product(store_id: str, product: Product, api_key: str = Depends(get_api_key)):
    pid = generateUUid()
    product = product.update(product_id=pid)
    await add_product_to_firestore(
        document=(store_id, pid),
        data=product.model_dump(),
        collection=FIREBASE_PRODUCT_COLLECTION
    )
    return product


@router.get("/{store_id}", response_model=List[Product])
async def get_products(store_id: str, api_key: str = Depends(get_api_key)):
    try:
        return await get_all_documents_product(
            document=store_id,
            collection=FIREBASE_PRODUCT_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")


@router.get("/{store_id}/{product_id}", response_model=Product)
async def get_product(store_id: str, product_id: str, api_key: str = Depends(get_api_key)):
    product = await get_product_document(
        document=(store_id, product_id),
        collection=FIREBASE_PRODUCT_COLLECTION
    )
    return product

@router.put("/{store_id}/{product_id}", response_model=Product)
async def update_product(store_id: str, product_id: str, updated: Product, api_key: str = Depends(get_api_key)):
    await update_product_in_firestore(
        document=(store_id, product_id),
        data=updated.model_dump(),
        collection=FIREBASE_PRODUCT_COLLECTION
    )
    return updated


@router.delete("/{store_id}/{product_id}")
async def delete_product(store_id: str, product_id: str,  api_key: str = Depends(get_api_key)):
    try:
        await delete_product_from_firestore(
            document=(store_id, product_id),
            collection=FIREBASE_PRODUCT_COLLECTION
        )
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Product not found")
