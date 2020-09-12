from typing import Any


class CryptoBase:
    async def create(self, guild_id: int, name: str) -> bool:
        """
        Add a crypto.
        :param guild_id: The guild id
        :param name: The crypto name
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
