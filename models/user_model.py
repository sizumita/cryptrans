from models.bases import UserBase
from lib.database.database import db
from typing import List
import asyncpg


class User(db.Model):
    """
    ユーザーが持っているお金の全てを保存する
    primary keyはユーザーidとお金の単位
    fields:
        id: user id
        guild_id: guild id
        amount: 所持枚数
    """
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    guild_id = db.Column(db.BigInteger, db.ForeignKey('crypto.id'), primary_key=True)
    amount = db.Column(db.BigInteger)


class UserModel(UserBase):
    async def get(self, user_id: int) -> List[User]:
        return await User.query.where(User.id == user_id).gino.all()

    async def get_one(self, user_id: int, guild_id: int) -> User:
        return await User.query.where(User.id == user_id).where(User.guild_id == guild_id).gino.first()

    async def get_crypto_all(self, guild_id: int) -> List[User]:
        return await User.query.where(User.guild_id == guild_id).gino.all()

    async def all(self) -> List[User]:
        return await User.query.gino.all()

    async def exists(self, user_id: int, guild_id: int) -> bool:
        return True if await self.get_one(user_id, guild_id) else False

    async def create(self, user_id: int, guild_id: int, amount: int) -> bool:
        try:
            await User(
                id=user_id,
                guild_id=guild_id,
                amount=amount
            ).create()
        except asyncpg.UniqueViolationError:
            return False
        return True

    async def add_amount(self, user_id: int, guild_id: int, amount: int) -> bool:
        if not await self.exists(user_id, guild_id):
            return await self.create(user_id, guild_id, amount)
        user = await self.get_one(user_id, guild_id)
        await user.update(amount=User.amount + amount).apply()
        return True
