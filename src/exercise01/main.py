from aioconsole import ainput

import asyncio
from aiohttp import ClientSession as CS
import os


# 200 status = ok
# https://images2.pics4learning.com/catalog/p/parrot.jpg
# https://bad-link-no-website-here.strange/img.png
# https://images2.pics4learning.com/catalog/s/swamp_15.jpg
class Parser:
    def __new__(cls):
        if not hasattr(cls, "_obj"):
            cls._obj = super(Parser, cls).__new__(cls)
        return cls._obj

    def __init__(self) -> None:
        self.requests = []
        self.session = None
        self.tasks = []
        self.way_to_safe = self.enter_way()

    def enter_way(self):
        while True:
            way = input()
            if os.path.exists(way):
                if os.access(way, os.W_OK):
                    return way
                else:
                    print(
                        "Введенный путь верный но у программы нет прав на запись в данную директорию\nПопробуй ввести другой путь!"
                    )
            else:
                print("Указанный путь не существует\nПопробуй ввести другой путь!")

    async def run(self):
        self.session = CS()
        while True:
            addres = await ainput()  # Асинхронный ввод
            if addres == "":
                break
            task = asyncio.create_task(self.make_request(addres))
            self.tasks.append(task)
        await asyncio.gather(*self.tasks)
        await self.session.close()

    async def save_to_file(self, request, file_name: str):
        way = os.path.join(self.way_to_safe, file_name)
        try:
            content = await request.read()
            with open(way, "wb") as file:
                file.write(content)
        except Exception as e:
            print(e)

    async def make_request(self, adress: str):
        for_print = tuple()
        try:
            async with self.session.get(url=adress) as request:
                if request.status == 200:
                    await self.save_to_file(request, adress.split("/")[-1])
                for_print = (adress, request.status)
        except Exception as e:
            return
        finally:
            if not for_print:
                for_print = (adress, 404)
            self.requests.append(for_print)

    def print(self):

        print(
            f"+------------------------------------------------------------------------------------+----------+"
        )
        print(
            f"| Ссылка                                                                             |  Статус  |"
        )
        print(
            f"+------------------------------------------------------------------------------------+----------+"
        )
        for item in self.requests:
            print(
                "| %-80s   | %-8s |"
                % (item[0], "Успех" if item[1] == 200 else "Ошибка")
            )
        print(
            f"+------------------------------------------------------------------------------------+----------+"
        )


if __name__ == "__main__":

    p = Parser()
    asyncio.run(p.run())
    p.print()
