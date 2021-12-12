from fastapi import FastAPI, Depends
from .auth import AuthHandler
from app.server.routes.user import router as UserRouter
from app.server.routes.auth import router as AuthRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_handler = AuthHandler()
app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(AuthRouter, tags=["Login"], prefix="/login")

@app.get('/')
def root():
    return {"Hello":"World"}


# @app.get('/api/users')
# async def fetch_users(username=Depends(auth_handler.auth_wrapper)):
#     return {"message": username} 
