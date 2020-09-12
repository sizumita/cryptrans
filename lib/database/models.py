from .database import db


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


class Users(db.Model):
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
