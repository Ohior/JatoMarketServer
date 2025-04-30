from fastapi import APIRouter, Depends, HTTPException
from typing import List

from data_model.Store import Store
from database.manage_database import add_data_to_firestore, delete_data_from_firestore, get_all_documents_from_collection, get_data_from_firestore, update_data_in_firestore
from security.api_manage import get_api_key
from utils.Constants import FIREBASE_STORE_COLLECTION
from utils.Tools import generateUUid

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post("/", response_model=Store)
async def create_store(store: Store, api_key: str = Depends(get_api_key)):
    _id = generateUUid()
    store = store.update(
        store_id=f"{store.store_name}_{_id}",
    )
    await add_data_to_firestore(
        data=store.model_dump(),
        document=store.store_id,
        collection=FIREBASE_STORE_COLLECTION
    )
    return store


@router.get("/", response_model=List[Store])
async def get_stores(api_key: str = Depends(get_api_key)):
    return await get_all_documents_from_collection(collection=FIREBASE_STORE_COLLECTION)


@router.get("/{store_id}", response_model=Store)
async def get_store(store_id: str, api_key: str = Depends(get_api_key)):
    try:
        await get_data_from_firestore(
            document=store_id,
            collection=FIREBASE_STORE_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")


@router.put("/{store_id}", response_model=Store)
async def update_store(store_id: str, updated: Store, api_key: str = Depends(get_api_key)):
    try:
        await update_data_in_firestore(
            data=updated.model_dump(),
            document=store_id,
            collection=FIREBASE_STORE_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")


@router.delete("/{store_id}")
async def delete_store(store_id: str, api_key: str = Depends(get_api_key)):
    try:
        await delete_data_from_firestore(
            document=store_id,
            collection=FIREBASE_STORE_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")
