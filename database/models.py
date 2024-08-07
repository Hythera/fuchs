from aiomysql import Pool
from database import get_pool

level_table = "level_users"

class LevelUser:
    def __init__(self, client_id: int):
        self.client_id = client_id
        self.xp = 0
        self.messages = 0

    async def load(self):
        pool: Pool = await get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT * FROM `{level_table}` WHERE `client_id`= %s", self.client_id)
                result = await cursor.fetchone()
                if result is None:
                    await cursor.execute(f"INSERT INTO `{level_table}` (`client_id`) VALUES (%s)", self.client_id)
                else:
                    self.xp = result[1]
                    self.messages = result[2]
                    
        pool.close()
        await pool.wait_closed()
        return self
    
    async def save(self):
        pool: Pool = await get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE `{level_table}` SET `xp` = %s, `messages` = %s WHERE `client_id` = %s", (self.xp, self.messages, self.client_id))
        pool.close()
        await pool.wait_closed()
        return self
    
    async def get_position(self) -> int:
        pool: Pool = await get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT COUNT(*) + 1 FROM `{level_table}` WHERE `xp` > (SELECT `xp` FROM `{level_table}` WHERE `client_id` = %s)", (self.client_id,))
                result = await cursor.fetchone()
                position = result[0]
        pool.close()
        await pool.wait_closed()
        return position
    
    @staticmethod
    async def get_top_users() -> list:
        pool: Pool = await get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT `client_id`, `xp` FROM `{level_table}` ORDER BY `xp` DESC LIMIT 10")
                results = await cursor.fetchall()
        pool.close()
        await pool.wait_closed()
        return results

    async def add_data(self, xp: int = None, messages: int = None) -> bool:
        level_before = self.get_level()
        if xp is not None:
            self.xp += xp
        level_after = self.get_level()

        if messages is not None:
            self.messages += 1

        await self.save()
        return level_after > level_before

    def get_level(self):
        return int((self.xp / 50) ** (1 / 1.5))
    
    def get_xp_for_level(self, level: int = None):
        if level:
            return int((level ** 1.5) * 50)
        else:
            return int(((self.get_level() + 1) ** 1.5) * 50)