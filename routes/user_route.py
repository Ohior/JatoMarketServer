from fastapi import APIRouter, Depends, HTTPException
from typing import List

from data_model.User import User
from database.manage_database import delete_data_from_firestore, get_all_documents_from_collection, get_data_from_firestore, update_data_in_firestore
from security.api_manage import get_api_key
from utils.Constants import FIREBASE_USER_COLLECTION

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_users(api_key: str = Depends(get_api_key)):
    return await get_all_documents_from_collection(collection=FIREBASE_USER_COLLECTION)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, api_key: str = Depends(get_api_key)):
    try:
        return await get_data_from_firestore(
            document=user_id,
            collection=FIREBASE_USER_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, updated: User, api_key: str = Depends(get_api_key)):
    try:
        await update_data_in_firestore(
            document=user_id,
            data=updated.model_dump(),
            collection=FIREBASE_USER_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}")
async def delete_user(user_id: str, api_key: str = Depends(get_api_key)):
    try:
        await delete_data_from_firestore(
            document=user_id,
            collection=FIREBASE_USER_COLLECTION
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
