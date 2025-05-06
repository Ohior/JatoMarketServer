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
        document_id=f"{store.store_name.replace(' ', '_')}_{_id}",
        store_id=_id,
    )
    await add_data_to_firestore(
        data=store.model_dump(),
        document=store.document_id,
        collection=FIREBASE_STORE_COLLECTION
    )
    return store


@router.get("/", response_model=List[Store])
async def get_stores(api_key: str = Depends(get_api_key)):
    return await get_all_documents_from_collection(collection=FIREBASE_STORE_COLLECTION)


@router.get("/{document_id}", response_model=Store)
async def get_store(document_id: str, api_key: str = Depends(get_api_key)):
    try:
        return await get_data_from_firestore(
            document=document_id,
            collection=FIREBASE_STORE_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")


@router.put("/{document_id}", response_model=Store)
async def update_store(document_id: str, updated: Store, api_key: str = Depends(get_api_key)):
    try:
        await update_data_in_firestore(
            data=updated.model_dump(),
            document=document_id,
            collection=FIREBASE_STORE_COLLECTION
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")


@router.delete("/{document_id}")
async def delete_store(document_id: str, api_key: str = Depends(get_api_key)):
    try:
        await delete_data_from_firestore(
            document=document_id,
            collection=FIREBASE_STORE_COLLECTION
        )
        return {"message": "Store deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Store not found")
