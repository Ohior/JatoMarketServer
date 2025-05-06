from typing import Any
import firebase_admin
from fastapi import HTTPException, Header
import os
from firebase_admin import auth
from firebase_admin import credentials
# from firebase_admin import firestore
from google.cloud import firestore

from data_model.User import User
from utils.Constants import FIREBASE_USER_COLLECTION


# Use a service account.
_FIREBASE_SERVICE_KEY = "raw/credentials/jatos-market-place-firebase-adminsdk.json"
cred = credentials.Certificate(_FIREBASE_SERVICE_KEY)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _FIREBASE_SERVICE_KEY
firebase_admin.initialize_app(cred)
_db = firestore.Client()


def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid authorization header")

    id_token = authorization.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token  # contains uid, email, etc.
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def create_user_email_password(user: User) -> User:
    try:
        u = auth.create_user(email=user.email, password=user.password)
        user = user.update(
            uid=u.uid, is_active=True,
            document_id=f"{user.email}_{u.uid}"
        )
        return user
    except Exception as e:
        auth.delete_user(u.uid)
        raise HTTPException(status_code=400, detail=str(e))


async def add_data_to_firestore(
    data: Any,
    document: str,
    collection: str,
) -> bool:
    try:
        _db.collection(collection).document(
            document).document("document").set(data)
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_product_to_firestore(
    data: Any,
    document: tuple[str],
    collection: str,
) -> bool:
    try:
        (
            _db.collection(collection)
            .document(document[0])
            .collection("product")
            .document(document[1])
            .set(data)
        )
# _db.collection(collection).document(document).document("document").set(data)
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_data_in_firestore(
    data: Any,
    document: str,
    collection: str,
) -> bool:
    try:
        _db.collection(collection).document(document).update(data)
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_data_from_firestore(
    document: str,
    collection: str,
) -> dict:
    try:
        return _db.collection(collection).document(document).get().to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_documents_from_collection(collection: str) -> list[dict]:
    # Get a reference to the Firestore collection
    try:
        collection_ref = _db.collection(collection)
        docs = collection_ref.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['document'] = doc.id  # Include document ID if needed
            results.append(data)

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_documents_product(document: str, collection: str) -> list[dict]:
    # Get a reference to the Firestore collection
    try:
        results = []
        collect_ref = (
            _db.collection(collection)
            .document(document)
            .collection("product")
        )
        docs = collect_ref.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            results.append(data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_product_document(document: tuple[str], collection: str) -> list[dict]:
    # Get a reference to the Firestore collection
    try:
        results = (
            _db.collection(collection)
            .document(document[0])
            .collection("product")
            .document(document[1])
            .get()
            .to_dict()
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_product_in_firestore(
    data: Any,
    document: tuple[str],
    collection: str,
) -> bool:
    try:
        (
            _db.collection(collection)
            .document(document[0])
            .collection("product")
            .document(document[1]).update(data)
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_product_from_firestore(
    document: tuple[str],
    collection: str,
) -> bool:
    try:
        (
            _db.collection(collection)
            .document(document[0])
            .collection("product")
            .document(document[1])
            .delete()
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_data_from_firestore(
    document: str,
    collection: str,
) -> bool:
    try:
        _db.collection(collection).document(document).delete()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
