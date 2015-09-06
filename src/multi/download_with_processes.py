"""This is an example of using multiple processes to download several websites."""
#!/usr/bin/env python

import ctypes
import requests
import sys
from multiprocessing import Process, Lock, Value

SITES = ("http://www.hotnews.ro/", "https://www.google.com/",
         "http://stackoverflow.com/", "http://blog.codinghorror.com/",
         "http://georgestocker.com/", "www.livescore.com/tennis/")

DEFAULT_WORKERS_NO = len(SITES)

PRINTER_LOCK = Lock()
COUNTER_LOCK = Lock()

DOWNLOADED_URLS_NO = Value('i', 0)


def download(index, url, downloaded_urls_no):
    """Download the content of the given url

    Args:
        index: the index of the thread doing the work
        url: the url to download
        downloaded_urls_no: shared variable, the number of downloaded
            urls so far
    """
    with PRINTER_LOCK:
        print index.value, "is downloading", url.value

    try:
        requests.get(url=url.value)
    except Exception as ex:
        with PRINTER_LOCK:
            print index.value, "failed to download", url.value, ". Error:", ex
        return

    with COUNTER_LOCK:
        downloaded_urls_no.value += 1


def print_usage():
    """Print the usage for this executable"""
    print "Usage:\n"
    print "./download_with_processes.py [workers_no]"


def main():
    """The main function of the executable"""
    if len(sys.argv) > 2:
        print_usage()
        return

    if len(sys.argv) == 2:
        workers_no = int(sys.argv[1])
    else:
        workers_no = DEFAULT_WORKERS_NO

    workers = []
    for i in range(workers_no):
        index = Value('i', i + 1)
        url = Value(ctypes.c_char_p, SITES[i % len(SITES)])
        worker = Process(target=download, args=(index, url, DOWNLOADED_URLS_NO, ))
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    print "Downloaded documents:", DOWNLOADED_URLS_NO.value

if __name__ == "__main__":
    main()
