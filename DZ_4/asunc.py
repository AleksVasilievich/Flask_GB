import requests
import asyncio
import aiohttp
import time
import sys

async def download_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # filename = "DZ_4/foto/" + url.split('/')[-1]
                    filename = "foto/" + url.split('/')[-1]
                    with open(filename, 'wb') as f:
                        f.write(await response.read())
                    print(f"Изображение {filename} успешно загружено")
                else:
                    print(f"Не удалось загрузить изображение с URL: {url}")
    except Exception as e:
        print(f"Ошибка при загрузке изображения с URL: {url}, {e}")

async def main_asunc(urls):
    start_time = time.time()
    tasks = [download_image(url) for url in urls]
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Общее время выполнения, асинхронная реализация программы: {end_time - start_time} секунд")
    print()

if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Укажите список URL-адресов через аргументы командной строки")
    else:
        asyncio.run(main_asunc(urls))