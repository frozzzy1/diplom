from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.schemas.response import ResponseSchema
from app.api.schemas.users import AddUserSchema, LoginUserSchema, ReadUserSchema, RegisterUserSchema
from app.database.repositories.users import UserRepository
from app.api.exceptions.exceptions import (
    PasswordsDoNotMatchException,
    UserAlreadyExistsException,
    IncorrectLoginOrPasswordException,
)
from app.utils.auth import get_password_hash, verify_password


class UserMiddleware:

    def __init__(self, session: AsyncSession) -> None:
        self.user_repository = UserRepository(session)

    async def add_one(self, user: RegisterUserSchema) -> ResponseSchema:
        if user.password1 != user.password2:
            raise PasswordsDoNotMatchException()
        user = AddUserSchema(
            full_name=user.full_name,
            login=user.login,
            hashed_password=get_password_hash(user.password1),
            phone=user.phone,
        )
        try:
            user = await self.user_repository.add_one(user)
        except IntegrityError:
            raise UserAlreadyExistsException()
        return ResponseSchema(
            data={'user': user.model_dump(exclude=['hashed_password'])}
        )
    
    async def find_all(self) -> list[ReadUserSchema]:
        users = await self.user_repository.find_all()
        return users
    
    async def find_one_or_none_by_id(self, id: int) -> ReadUserSchema:
        return await self.user_repository.find_one_or_none_by_id(id)
    
    async def is_authenticate_user(self, u: LoginUserSchema) -> str:
        user = await self.user_repository.find_one_or_none(u)
        if user and verify_password(u.password, user.hashed_password):
            return str(user.id)
        raise IncorrectLoginOrPasswordException()
