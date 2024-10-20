import aiosqlite


class BD(object):
    """Класс для работы с БД"""


    def __init__(self, path: str) -> None:
        self.path = path


    async def send_sql(self, query: str) -> None | list[tuple]:
        """Метод по отправлению SQL-запросов в СУБД"""

        async with aiosqlite.connect(database=f'data/database/{self.path}') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(sql=query)
                await connection.commit()

                try:
                    data = await cursor.fetchall()
                except aiosqlite.ProgrammingError:
                    pass
                else:
                    return data


    async def created_table(self) -> None:
        """Метод по созданию таблиц в БД"""

        query = '''
            CREATE TABLE IF NOT EXISTS "gift" (
                "id"	INTEGER NOT NULL,
                "user_id"	INTEGER NOT NULL,
                "title"	TEXT NOT NULL,
                "description"	TEXT NOT NULL,
                "link"	TEXT NOT NULL,
                "datetime"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );   
            '''
        
        await self.send_sql(query)


    async def add_gift(self, user_id: str, title: str, description: str, link: str, datetime: str) -> None:
        """Метод по добавлению новых записей в таблицу gift"""

        query = '''
                INSERT INTO gift (user_id, title, description, link, datetime)
	            VALUES (%s, '%s', '%s', '%s', '%s');          
            ''' % (user_id, title, description, link, datetime)
        
        await self.send_sql(query)

    
    async def get_gifts(self, user_id: str) -> list:
        """Метод по получению данных из таблицы gift"""

        query = '''
                SELECT * FROM gift
                WHERE user_id = %s;          
            ''' % (user_id)
         
        return await self.send_sql(query)
    

    async def get_gift(self, gift_id: str) -> list:
        """Метод по получению данных об одном желании"""

        query = '''
                SELECT * FROM gift
                WHERE id = %s;          
            ''' % (gift_id)
         
        return await self.send_sql(query)
    

    async def delete_gift(self, gift_id: str) -> None:
        """Метод по удалению желания из БД"""

        query = '''
                DELETE FROM gift
                WHERE id = %s;         
            ''' % (gift_id)
         
        await self.send_sql(query)
