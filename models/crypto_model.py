from models.bases import CryptoBase
from lib.database.database import db
from typing import List
import asyncpg


class Crypto(db.Model):
    """
    格ギルドのお金の定義
    fields:
        id: guild id
        name: crypto name
        total: 発行枚数
        created_at: 最初に発行された時間
    """
    __tablename__ = "crypto"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    total = db.Column(db.BigInteger, default=0)
    created_at = db.Column(db.DateTime(), server_default='now()')


class CryptoModel(CryptoBase):
    async def create(self, guild_id: int, name: str) -> bool:
        try:
            await Crypto.create(
                id=guild_id,
                name=name
            )
        except asyncpg.UniqueViolationError:
            return False
        return True

    async def add_total(self, guild_id: int, amount: int) -> bool:
        return True

    async def get(self, guild_id: int) -> Crypto:
        return await Crypto.query.where(Crypto.id == guild_id).gino.first()

    async def all(self) -> List[Crypto]:
        return await Crypto.query.gino.all()

    async def name_exists(self, name: str) -> bool:
        return True

    async def guild_exists(self, guild_id: int) -> bool:
        return True
