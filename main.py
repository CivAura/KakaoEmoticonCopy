import re
import requests
import os
from urllib.parse import urlsplit

urlPattern = r'(https?://[^\s\'"<>]+)'

downloadDir = "download"
os.makedirs(downloadDir, exist_ok=True)

def extractUrls(text):
    urls = re.findall(urlPattern, text)
    return urls

def downloadFile(url, downloadDir):
    try:
        url = url[:-1] if url[-1] in ',.;)]}' else url

        ignoredFilenames = ['thumb_empty.png', 'img_send.png']
        if any(url.endswith(ignoredFilename) for ignoredFilename in ignoredFilenames):
            return

        fileName = os.path.basename(urlsplit(url).path)
        if not fileName:
            fileName = '1.png'
        elif not fileName.endswith('.png'):
            fileName += '.png'

        filePath = os.path.join(downloadDir, fileName)
        
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}, stream=True)
        response.raise_for_status()

        with open(filePath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f'성공\t{filePath}')
    except Exception as e:
        print(f'실패\t{e}')

def download(text):
    urls = extractUrls(text)
    for url in urls:
        downloadFile(url, downloadDir)

magic_unji_string = """
im super fat nigger << it's magic!
"""

download(magic_unji_string)
