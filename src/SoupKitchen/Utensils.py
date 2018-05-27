# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup

def MakeSoup(ref_page):
    '''
    Makes a BeautifulSoup object from a url.
    '''

    page = urlopen(ref_page)
    soup = BeautifulSoup(page, 'html.parser')

    return soup


def DownloadFile(url, filename):
    '''
    Download a file from a URL with a progress meter.
    '''

    href = urlopen(url)
    f = open(filename, 'wb')
    meta = href.info()
    file_size = int(meta.get_all("Content-Length")[0])

    print("Downloading: %s Bytes: %s" % (filename, file_size))

    file_size_dl = 0
    block_sz = 8192
    status_len = 0

    while True:
        buffer = href.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)

        status = "%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)

        print(status, end='')

        backspace(status_len)
        status_len = len(status)

    f.close()

    print('\n', end='')
