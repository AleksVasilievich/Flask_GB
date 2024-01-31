import DZ_4.sunh


if __name__ == '__main__':
    urls = ['https://w.forfun.com/fetch/25/2529ce3d3391789f369c4ec9a07a1b82.jpeg',
            'https://w.forfun.com/fetch/cc/ccfb2142acf6e9eac9b6e240255e3af7.jpeg',
            'https://w.forfun.com/fetch/f1/f1288f09927aafd68470ea0b626645fd.jpeg']


    if not urls:
        print("Укажите список URL-адресов через аргументы командной строки")
    else:
        DZ_4.sunh.main_sunh(urls)