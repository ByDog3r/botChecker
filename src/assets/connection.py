import datetime
import sqlite3
import random
import string
import json
from typing import Union, Optional, Dict

data_config = json.load(open("src/assets/cfgbot.json", "r"))


class Database:
    BOT_TABLE = "users"
    BOT_KEYS_TABLE = "bot_keys"
    BOT_GROUPS = "groups"
    ID_OWNER = int(data_config["ID_OWNER"])

    def __init__(self) -> None:
        self.connection = sqlite3.connect("src/assets/bycheck.db")
        self.cursor = self.connection.cursor()
        self.__CreateTables()
        if not self.IsSellerOrAdmin(self.ID_OWNER):
            self.PromoteToAdmin(self.ID_OWNER)

    def AddPremiumMembership(
        self, user_id: int, days: int, credits: int
    ) -> Optional[str]:
        user_id = int(user_id)
        days = int(days)
        credits = int(credits)

        user_data = self.cursor.execute(
            "SELECT MEMBERSHIP FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None

        expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
        expiration_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "UPDATE {} SET MEMBERSHIP='Premium', ANTISPAM=25, CREDITS=?, EXPIRATION=? WHERE ID=?".format(
                self.BOT_TABLE
            ),
            (credits, expiration_time, user_id),
        )
        self.connection.commit()
        return expiration_time

    def IsPremium(self, user_id: int) -> bool:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT MEMBERSHIP FROM {} WHERE ID=?".format(self.BOT_TABLE),
            (user_id,),
        )
        user_data = user_data.fetchone()
        return str(user_data[0]).lower() == "premium" if user_data else False

    def RegisterUser(self, user_id: int, username: str) -> None:
        try:
            user_id = int(user_id)
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO {} (ID, USERNAME, REGISTERED) VALUES (?, ?, ?)".format(
                    self.BOT_TABLE
                ),
                (user_id, username, time),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass

    def GenKey(self, days: int) -> tuple:
        expire_day = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=int(days)),
            "%Y-%m-%d %H:%M:%S",
        )
        key = "bot-key" + "".join(random.choice(string.ascii_letters) for x in range(8))
        self.cursor.execute(
            "INSERT INTO {} (BOT_KEY, EXPIRATION) VALUES (?, ?)".format(
                self.BOT_KEYS_TABLE
            ),
            (key, expire_day),
        )
        self.connection.commit()
        return key, expire_day

    def RemovePremium(self, user_id: int) -> Optional[int]:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT MEMBERSHIP FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None

        self.cursor.execute(
            "UPDATE {} SET MEMBERSHIP='free user', RANK='user', ANTISPAM=60, CREDITS=0, EXPIRATION=NULL WHERE ID=?".format(
                self.BOT_TABLE
            ),
            (user_id,),
        )
        self.connection.commit()
        return 1

    def RemoveGroup(self, chat_id: str) -> Optional[int]:
        data = self.cursor.execute(
            "SELECT EXPIRATION FROM {} WHERE ID=?".format(self.BOT_GROUPS),
            (chat_id,),
        )
        data = data.fetchone()
        if data is None:
            return None

        self.cursor.execute(
            "DELETE FROM {} WHERE ID=?".format(self.BOT_GROUPS),
            (chat_id,),
        )
        self.connection.commit()
        return 1

    def UnbanOrBanUser(self, user_id: int, ban: bool = True) -> Optional[int]:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT MEMBERSHIP FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None
        status = "ban" if ban else "free"

        self.cursor.execute(
            "UPDATE {} SET RANK='user', MEMBERSHIP='free user', ANTISPAM=60, CREDITS=0, EXPIRATION=NULL, STATE=? WHERE ID=?".format(
                self.BOT_TABLE
            ),
            (status, user_id),
        )
        self.connection.commit()
        return 1

    def IsBan(self, user_id: int) -> bool:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT STATE FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        return str(user_data[0]).lower() == "ban" if user_data else False

    def ClaimKey(self, key: str, user_id: int) -> Optional[str]:
        data = self.cursor.execute(
            "SELECT EXPIRATION FROM {} WHERE BOT_KEY=?".format(self.BOT_KEYS_TABLE),
            (key,),
        )
        key_data = data.fetchone()
        if key_data is None:
            return None
        expiration_time = key_data[0]
        self.cursor.execute(
            "UPDATE {} SET MEMBERSHIP='Premium', ANTISPAM=25, EXPIRATION=? WHERE ID=?".format(
                self.BOT_TABLE
            ),
            (expiration_time, user_id),
        )
        self.cursor.execute(
            "DELETE FROM {} WHERE BOT_KEY=?".format(self.BOT_KEYS_TABLE), (key,)
        )
        self.connection.commit()
        return expiration_time

    def __IsRank(self, user_id: int, rank: str) -> bool:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT RANK FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        return str(user_data[0]).lower() == rank if user_data else False

    def IsAdmin(self, user_id: int) -> bool:
        return self.__IsRank(user_id, "admin")

    def IsSeller(self, user_id: int) -> bool:
        return self.__IsRank(user_id, "seller")

    def IsSellerOrAdmin(self, user_id) -> bool:
        if self.IsAdmin(user_id) or self.IsSeller(user_id):
            return True
        return False

    def __GetInfo(self, ID: int, group: bool = False) -> list:
        ID = int(ID)
        table = self.BOT_GROUPS if group else self.BOT_TABLE
        data = self.cursor.execute("SELECT * FROM {} WHERE ID=?".format(table), (ID,))
        data = data.fetchone()
        return data

    def RemoveKey(self, key: str) -> Optional[bool]:
        data = self.cursor.execute(
            "SELECT BOT_KEY FROM {} WHERE BOT_KEY=?".format(self.BOT_KEYS_TABLE),
            (key,),
        )
        data = data.fetchone()
        if data is None:
            return None
        self.cursor.execute(
            "DELETE FROM {} WHERE BOT_KEY=?".format(self.BOT_KEYS_TABLE), (key,)
        )
        self.connection.commit()
        return True

    def GetInfoUser(self, user_id: int) -> Dict[str, Union[str, int]] | None:
        user_data = self.__GetInfo(user_id)
        return (
            {
                "ID": user_data[0],
                "USERNAME": user_data[1],
                "NICK": user_data[2],
                "RANK": user_data[3],
                "STATE": user_data[4],
                "MEMBERSHIP": user_data[5],
                "EXPIRATION": user_data[6],
                "ANTISPAM": user_data[7],
                "CREDITS": user_data[8],
                "REGISTERED": user_data[9],
            }
            if user_data
            else None
        )

    def GetInfoGroup(self, chat_id: int) -> Dict[str, Union[str, int]] | None:
        group_data = self.__GetInfo(chat_id, True)
        if not group_data:
            return None
        return {
            "ID": group_data[0],
            "EXPIRATION": group_data[1],
        }

    def GetChatsIds(self) -> list:
        users_data = self.cursor.execute("SELECT ID FROM {}".format(self.BOT_TABLE))
        users_data = users_data.fetchall()
        chats_id_data = self.cursor.execute("SELECT ID FROM {}".format(self.BOT_GROUPS))
        users_data.extend(chats_id_data.fetchall())
        return [data[0] for data in users_data]

    def GroupAuthorized(self, chat_id: int) -> bool:
        chat_id = int(chat_id)
        data = self.cursor.execute(
            "SELECT EXPIRATION FROM {} WHERE ID=?".format(self.BOT_GROUPS),
            (chat_id,),
        )
        expiration = data.fetchone()
        if expiration is None:
            return False
        return True

    def UserHasCredits(self, user_id: int) -> bool:
        credits_user = self.cursor.execute(
            "SELECT CREDITS FROM {} WHERE ID=?".format(self.BOT_TABLE),
            (user_id,),
        ).fetchone()[0]
        return credits_user > 0

    def RemoveCredits(self, user_id: int, credits: int) -> None:
        if credits <= 0:
            return
        credits_user = self.cursor.execute(
            "SELECT CREDITS FROM {} WHERE ID=?".format(self.BOT_TABLE),
            (user_id,),
        ).fetchone()[0]
        new_credits = credits_user - credits if credits_user > 0 else 0
        self.cursor.execute(
            "UPDATE {} SET CREDITS=? WHERE ID=?".format(self.BOT_TABLE),
            (new_credits, user_id),
        )
        self.connection.commit()

    def AddGroup(self, chat_id: int, days: int, username: str) -> Union[str, bool]:
        try:
            chat_id = int(chat_id)
            expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
            expiration_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO {} (ID, EXPIRATION, PROVIDER) VALUES (?, ?, ?)".format(
                    self.BOT_GROUPS
                ),
                (chat_id, expiration_time, username),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            self.cursor.execute(
                "UPDATE {} SET EXPIRATION=?, PROVIDER=? WHERE ID=?".format(
                    self.BOT_GROUPS
                ),
                (expiration_time, username, chat_id),
            )
            self.connection.commit()
        return expiration_time

    def IsAuthorized(self, user_id: int, chat_id: int) -> bool:
        user_id = int(user_id)
        chat_id = int(chat_id)

        if self.IsPremium(user_id) or self.GroupAuthorized(chat_id):
            return True
        return False

    def RemoveExpiredsUsers(self) -> None:
        table_queries = [
            (
                "SELECT ID, EXPIRATION FROM {} WHERE EXPIRATION IS NOT NULL",
                self.BOT_TABLE,
                self.RemovePremium,
            ),
            (
                "SELECT ID, EXPIRATION FROM {} WHERE EXPIRATION IS NOT NULL",
                self.BOT_GROUPS,
                self.RemoveGroup,
            ),
        ]
        now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        for query_format, table, remove_function in table_queries:
            data = self.cursor.execute(query_format.format(table))
            expireds = filter(lambda x: x[1] < now, data.fetchall())
            for data in expireds:
                remove_function(data[0])

    def PreventOwnerUpdate(self, user_id: int, target_id: int) -> bool:
        if target_id == self.ID_OWNER and user_id != self.ID_OWNER:
            return True
        return False

    def IncreaseChecks(self, user_id: int, quantity: int = 1) -> bool | None:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT CHECKS FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None
        checks = user_data[0] + quantity
        self.cursor.execute(
            "UPDATE {} SET CHECKS=? WHERE ID=?".format(self.BOT_TABLE),
            (checks, user_id),
        )
        self.connection.commit()
        return True

    def __Promote(self, user_id: int, rank: str) -> bool | None:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT RANK FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None
        self.cursor.execute(
            "UPDATE {} SET RANK='{}' WHERE ID=?".format(self.BOT_TABLE, rank),
            (user_id,),
        )
        self.connection.commit()
        return True

    def SetNick(self, user_id: int, nick: str) -> bool | None:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT NICK FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None
        self.cursor.execute(
            "UPDATE {} SET NICK=? WHERE ID=?".format(self.BOT_TABLE),
            (
                nick,
                user_id,
            ),
        )
        self.connection.commit()
        return True

    def SetAntispam(self, user_id: int, antispam: int) -> bool | None:
        user_id = int(user_id)
        user_data = self.cursor.execute(
            "SELECT ANTISPAM FROM {} WHERE ID=?".format(self.BOT_TABLE), (user_id,)
        )
        user_data = user_data.fetchone()
        if user_data is None:
            return None
        self.cursor.execute(
            "UPDATE {} SET ANTISPAM=? WHERE ID=?".format(self.BOT_TABLE),
            (
                antispam,
                user_id,
            ),
        )
        self.connection.commit()
        return True

    def PromoteToSeller(self, user_id: int) -> bool | None:
        return self.__Promote(user_id, "seller")

    def PromoteToAdmin(self, user_id: int) -> bool | None:
        return self.__Promote(user_id, "admin")

    def CloseDb(self) -> None:
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None

    def __CreateTables(self) -> None:
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.BOT_TABLE}(
            ID VARCHAR(25) NOT NULL PRIMARY KEY,
            USERNAME VARCHAR(32) DEFAULT NULL UNIQUE,
            NICK VARCHAR(32) DEFAULT '¿?',
            RANK VARCHAR(15) DEFAULT 'user',
            STATE VARCHAR(12) DEFAULT 'free',
            MEMBERSHIP VARCHAR(15) DEFAULT 'free user',
            EXPIRATION varchar(20) DEFAULT NULL,
            ANTISPAM INT(3) DEFAULT 60,
            CREDITS INT(15) DEFAULT 0,
            REGISTERED TEXT NOT NULL,
            CHECKS INT(15) DEFAULT 0
            )"""
        )

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.BOT_KEYS_TABLE}(
            BOT_KEY VARCHAR(30) NOT NULL PRIMARY KEY,
            EXPIRATION TEXT NOT NULL
            )"""
        )

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.BOT_GROUPS}(
            ID VARCHAR(30) NOT NULL PRIMARY KEY,
            EXPIRATION TEXT NOT NULL,
            PROVIDER VARCHAR(30) NOT NULL
            )"""
        )
        self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.CloseDb()
