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
        hold: まだ運営が持っている数（運営含め誰にも渡していない、運営が自由に配布できる数）
        per_amount: 10分ごとに増えるholdの数
        created_at: 最初に発行された時間
    """
    __tablename__ = "crypto"

    id = db.Column(db.BigInteger, primary_key=True)
    unit = db.Column(db.String)
    name = db.Column(db.String)
    hold = db.Column(db.BigInteger, default=0)
    created_at = db.Column(db.DateTime(), server_default='now()')
    max_amount = db.Column(db.BigInteger)
    member_count = db.Column(db.BigInteger)
    distribution = db.Column(db.Boolean, default=True)


class CryptoModel(CryptoBase):
    async def create(self, guild_id: int, name: str, unit: str, member_count: int) -> bool:
        if await self.name_exists(name=name):
            return False
        if await self.guild_exists(guild_id=guild_id):
            return False
        if member_count <= 100:
            max_amount = 4380000
        elif member_count <= 1000:
            max_amount = 43800000
        elif member_count <= 10000:
            max_amount = 438000000
        else:
            max_amount = 4380000000
        try:
            await Crypto.create(
                id=guild_id,
                name=name,
                unit=unit,
                max_amount=max_amount,
                member_count=member_count,
            )
        except asyncpg.UniqueViolationError:
            return False
        return True

    async def get(self, guild_id: int) -> Crypto:
        return await Crypto.query.where(Crypto.id == guild_id).gino.first()

    async def get_by_unit(self, unit: str) -> Crypto:
        return await Crypto.query.where(Crypto.unit == unit).gino.first()

    async def all(self) -> List[Crypto]:
        return await Crypto.query.gino.all()

    async def name_exists(self, name: str) -> bool:
        return True if await Crypto.query.where(Crypto.name == name).gino.first() else False

    async def unit_exists(self, unit: str) -> bool:
        return True if await Crypto.query.where(Crypto.unit == unit).gino.first() else False

    async def guild_exists(self, guild_id: int) -> bool:
        return True if await Crypto.query.where(Crypto.id == guild_id).gino.first() else False
