from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.schemas.users import LoginUserSchema, ReadUserSchema, RegisterUserSchema
from app.database.database import get_session
from app.middlewares.users import UserMiddleware
from app.api.exceptions.exceptions import (
    UserAlreadyExistsException,
    PasswordsDoNotMatchException,
    IncorrectLoginOrPasswordException,
)
from app.utils.auth import create_access_token, get_token
from app.core.config import settings
from jose import jwt, JWTError


router = APIRouter(
    prefix='/user',
    tags=['Auth & Users']
)


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGO])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    
    user_mw = UserMiddleware(session)
    user = await user_mw.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


@router.post('/register')
async def register_user(
    user: RegisterUserSchema,
    session: AsyncSession = Depends(get_session)
):
    user_mw = UserMiddleware(session)
    try:
        user = await user_mw.add_one(user)
    except UserAlreadyExistsException:
        return Response(
            status_code=UserAlreadyExistsException.status_code,
            content=UserAlreadyExistsException.detail,
        )
    except PasswordsDoNotMatchException:
        return Response(
            status_code=PasswordsDoNotMatchException.status_code,
            content=PasswordsDoNotMatchException.detail,
        )
    return user


@router.post('/login')
async def login_user(
    response: Response,
    user: LoginUserSchema,
    session: AsyncSession = Depends(get_session),
):
    user_mw = UserMiddleware(session)
    try:
        str_id = await user_mw.is_authenticate_user(user)
    except IncorrectLoginOrPasswordException:
        return Response(
            status_code=IncorrectLoginOrPasswordException.status_code,
            content=IncorrectLoginOrPasswordException.detail,
        )
    access_token = create_access_token({'sub': str_id})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout_user(
    response: Response,
):
    response.delete_cookie('access_token', httponly=True)
    return {'response': 'Logged out'}


@router.get('/all')
async def get_all_users(session: AsyncSession = Depends(get_session)):
    user_mw = UserMiddleware(session)
    users = await user_mw.find_all()
    return {'users': users}


@router.get('/me')
async def get_me(user: ReadUserSchema = Depends(get_current_user)):
    return {'user': user}