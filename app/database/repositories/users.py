from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.schemas.users import AddUserSchema, LoginUserSchema, ReadUserSchema
from app.database.models.users import UserOrm
from app.utils.repo import AbsRepo


class UserRepository(AbsRepo):
    async def add_one(self, data: AddUserSchema) -> ReadUserSchema:
        user = UserOrm(**data.model_dump())
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(user)
        return ReadUserSchema.model_validate(user)

    async def find_one_or_none(self, data: LoginUserSchema) -> ReadUserSchema | None:
        query = select(UserOrm).filter(UserOrm.login == data.login)
        result = await self.session.scalar(query)
        if result:
            return ReadUserSchema.model_validate(result)
        return
    
    async def find_one_or_none_by_id(self, id: int) -> ReadUserSchema | None:
        query = select(UserOrm).filter(UserOrm.id == id)
        result = await self.session.scalar(query)
        if result:
            return ReadUserSchema.model_validate(result)
        return

    async def find_all(self) -> list[ReadUserSchema]:
        query = select(UserOrm)
        result = await self.session.scalars(query)
        return [ReadUserSchema.model_validate(i).model_dump(exclude=['hashed_password']) for i in result]
