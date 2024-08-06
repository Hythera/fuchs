from aiomysql import Pool
from database import get_pool

class LevelUser:
    def __init__(self, client_id: int):
        self.client_id = client_id
        self.xp = 0

    async def load(self):
        pool: Pool = await get_pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM `level_users` WHERE `client_id`= %s", self.client_id)
                result = await cursor.fetchne()
                if result is None:
                    await cursor.execute("INSERT INTO `level_users` (`client_id`) VALUES (%s)", self.client_id)
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
                await cursor.execute("UPDATE `level_users` SET `xp` = %s, `messages` = %s WHERE `client_id` = %s", (self.xp, self.messages, self.client_id))
        pool.close()
        await pool.wait_closed()
        return self

    async def add_data(self, xp: int, messages: int = None):
        self.xp += xp
        if messages is not None:
            self.messages += 1
        await self.save()
        return self

    def get_data(self):
        return [int(self.xp ** 0.3), self.messages]