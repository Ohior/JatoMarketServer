from fastapi import APIRouter, Depends, HTTPException, Form
from firebase_admin import auth
from data_model.User import User
from database.manage_database import add_data_to_firestore, create_user_email_password, get_data_from_firestore, update_data_in_firestore, verify_token
from security.api_manage import get_api_key
from utils.Constants import FIREBASE_USER_COLLECTION

router = APIRouter()


@router.get("/secure-data")
def secure_route(user=Depends(verify_token)):
    return {"message": f"Hello {user['email']}, this is protected!"}


@router.post("/signup", response_model=User)
async def signup(
    user: User,
    api_key: str = Depends(get_api_key)
):
    try:
        user = await create_user_email_password(user.model_copy())
        await add_data_to_firestore(
            document=user.document_id,
            data=user.model_dump(),
            collection=FIREBASE_USER_COLLECTION
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login/{user_id}", response_model=User)
async def login(
    user_id: str,
    user: User,
    api_key: str = Depends(get_api_key)
):
    try:
        user_dict = await get_data_from_firestore(
            document=user_id,
            collection=FIREBASE_USER_COLLECTION
        )
        user_dict["is_active"] = True
        await update_data_in_firestore(
            document=user_id,
            data=user_dict,
            collection=FIREBASE_USER_COLLECTION
        )
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/logout/{user_id}", response_model=User)
async def logout(
    user_id: str,
    user: User,
    api_key: str = Depends(get_api_key)
):
    try:
        user_dict = await get_data_from_firestore(
            document=user_id,
            collection=FIREBASE_USER_COLLECTION
        )
        user_dict["is_active"] = False
        await update_data_in_firestore(
            document=user_id,
            data=user_dict,
            collection=FIREBASE_USER_COLLECTION
        )
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
