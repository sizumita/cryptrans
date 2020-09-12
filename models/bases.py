from typing import Any


class CryptoBase:
    async def create(self, guild_id: int, name: str, unit: str, per_amount: int) -> bool:
        """
        Add a crypto.
        :param unit: how say this crypto
        :param guild_id: The guild id
        :param name: The crypto name
        :param per_amount: 10分ごとに新しく増えるholdの数
        :return: bool
        """

    async def add_total(self, guild_id: int, amount: int) -> bool:
        """
        Add crypto total.
        :param guild_id: The guild id
        :param amount: diff
        :return: bool
        """

    async def get(self, guild_id: int) -> Any:
        """
        get crypto by guild id
        :param guild_id: The guild id
        :return: Any
        """

    async def get_by_unit(self, unit: str) -> Any:
        """
        get crypto by unit
        :param unit: The unit
        :return: Any
        """

    async def all(self) -> Any:
        """
        get all crypto
        :return: Any
        """

    async def name_exists(self, name: str) -> bool:
        """
        return True if name exists
        :param name: check name
        :return: bool
        """

    async def unit_exists(self, unit: str) -> bool:
        """
        return True if unit exists
        :param unit: check unit
        :return: bool
        """

    async def guild_exists(self, guild_id: int) -> bool:
        """
        return True if guild exists
        :param guild_id: check guild id
        :return: bool
        """


class UserBase:
    async def get(self, user_id: int) -> Any:
        """
        get user's all crypto amounts
        :param user_id: get user id
        :return: Any
        """

    async def get_one(self, user_id: int, guild_id: int) -> Any:
        """
        get user's a guild's crypto amounts
        :param user_id: get user id
        :param guild_id: guild id
        :return: Any
        """

    async def get_crypto_all(self, guild_id: int) -> Any:
        """
        get all users from a crypto
        :param guild_id: guild id
        :return: Any
        """

    async def all(self) -> Any:
        """
        get all user's all crypto amounts
        :return:
        """

    async def exists(self, user_id: int, guild_id: int) -> bool:
        """
        return True if user has guild's crypto
        :param user_id: check user id
        :param guild_id: check guild id
        :return: bool
        """

    async def create(self, user_id: int, guild_id: int, amount: int) -> bool:
        """
        create user data
        :param user_id: user id
        :param guild_id: guild id
        :param amount: initialize amount
        :return: bool
        """

    async def add_amount(self, user_id: int, guild_id: int, amount: int) -> bool:
        """
        add crypto to user
        :param user_id: user id
        :param guild_id: guild id
        :param amount: adding amount
        :return:
        """
