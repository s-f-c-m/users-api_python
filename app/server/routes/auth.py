from fastapi import HTTPException, Depends
from fastapi import APIRouter
from app.server.auth import AuthHandler
from app.server.models import AuthUser
from app.server.database import fetch_user

router = APIRouter()
auth_handler = AuthHandler()

@router.post('/')
async def login(auth_details: AuthUser):
    user = None
    user = await fetch_user(auth_details.user)

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid user or password')
    token = auth_handler.encode_token(user['user'], user['roles'], user['name'], user['email'])
    return { 'token': token}

@router.get('/validate')
async def validate(payload=Depends(auth_handler.auth_wrapper)):
    return payload
    # return {"logged": sub,"roles":roles} 
