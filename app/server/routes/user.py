from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from app.server.auth import AuthHandler

from app.server.database import (
    add_user,
    delete_user,
    fetch_user,
    fetch_users,
    update_user
)

from app.server.models import (
    User,
    UpdateUserModel,
    UpdateUserPassword,
    UpdateUserNameRoles,
    UpdateUserName,
    UpdateUserRoles,
    ErrorResponse,
    SuccessResponse
)

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/", response_description="Usuario registrado")
async def add_user_data(user: User = Body(...)):
    user.password = auth_handler.get_password_hash(user.password) 
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    if new_user == {}:
        return ErrorResponse('Error al ingresar usuario', 401, 'Usuario o email ya existe')
    return SuccessResponse(new_user, 'Usuario agregado satisfactoriamente') 

@router.get("/", response_description="Usuarios recibidos")
async def get_users(auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    users = await fetch_users()
    if users:
        return {"message": "Lista de usuarios leída", "usuarios": users}
    return {"message": "Lista de usuarios vacía", "code": 200, "usuarios": users}

@router.get("/{user}", response_description="Usuario recibido")
async def get_user(user, auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    user = await fetch_user(user)
    if user:
        return {'message':'usuario leído con éxito', "code": 200, 'user':user}
    return {'mesage':'usuario no encontrado', 'code':404 }

@router.put("/{user}")
async def update_user_data(user: str, req: UpdateUserModel = Body(...), auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    req = {k: v for k, v in req.dict().items() if v is not None}
    req['password'] = auth_handler.get_password_hash(req['password'])
    updated_user = await update_user(user, req)
    if updated_user:
        return {"message": "Usuario actualizado", "code": 200}
    return {"message": "Error al actualizar el usuario", "code": 404}

@router.put("/nameroles/{user}")
async def update_user_name_roles(user: str, req: UpdateUserNameRoles = Body(...), auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(user, req)
    if updated_user:
        return {"message": "Usuario actualizado", "code": 200}
    return {"message": "Error al actualizar el usuario", "code": 404}

@router.put('/password/{user}')
async def update_user_password(user:str, req: UpdateUserPassword = Body(...), auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    req = {k: v for k, v in req.dict().items() if v is not None}
    req['password'] = auth_handler.get_password_hash(req['password'])
    updated_user = await update_user(user, req)
    if updated_user:
        return {'message': 'Usuario actualizado', 'code':200}
    return {'message': 'Error al actualizar el usuario', 'code': 404}

@router.put('/name/{user}')
async def update_user_name(user:str, req: UpdateUserName = Body(...), auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(user, req)
    if updated_user:
        return {'message': 'Usuario actualizado', 'code':200}
    return {'message': 'Error al actualizar el usuario', 'code': 404}

@router.put('/roles/{user}')
async def update_user_roles(user:str, req: UpdateUserRoles = Body(...), auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(user, req)
    if updated_user:
        return {'message': 'Usuario actualizado', 'code':200}
    return {'message': 'Error al actualizar el usuario', 'code': 404}

@router.delete("/{user}")
async def delete_user_data(user: str, auth=Depends(auth_handler.auth_wrapper)):
    print(auth)
    deleted_user = await delete_user(user)
    if deleted_user:
        return {"message":"Usuario eliminado", "code":200}
    return {"message":"Error al eliminar el usuario", "code": 404}
