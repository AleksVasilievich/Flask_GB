import requests
import time
import sys

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = "DZ_4/foto/" + url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Изображение {filename} успешно загружено")
        else:
            print(f"Не удалось загрузить изображение с URL: {url}")
    except Exception as e:
        print(f"Ошибка при загрузке изображения с URL: {url}, {e}")

def main_sunh(urls):
    start_time = time.time()
    for url in urls:
        download_image(url)
    end_time = time.time()
    print(f"Общее время выполнения программы: {end_time - start_time} секунд")

if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Укажите список URL-адресов через аргументы командной строки")
    else:
        main_sunh(urls)