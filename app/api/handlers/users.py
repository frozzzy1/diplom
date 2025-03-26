from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.schemas.users import LoginUserSchema, RegisterUserSchema
from app.database.database import get_session
from app.middlewares.users import UserMiddleware
from app.api.exceptions.exceptions import (
    UserAlreadyExistsException,
    PasswordsDoNotMatchException,
    IncorrectLoginOrPasswordException,
)
from app.utils.auth import create_access_token


router = APIRouter(
    prefix='/user',
    tags=['Auth & Users']
)


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


@router.get('/all')
async def get_all_users(session: AsyncSession = Depends(get_session)):
    user_mw = UserMiddleware(session)
    users = await user_mw.find_all()
    return {'users': users}