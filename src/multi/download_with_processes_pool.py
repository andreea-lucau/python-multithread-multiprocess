"""This is an example of using processes Pool to download several websites."""
#!/usr/bin/env python

import ctypes
import requests
import sys
from multiprocessing import Process, Lock, Array, Pool, Value

SITES = ("http://www.hotnews.ro/", "https://www.google.com/",
         "http://stackoverflow.com/", "http://blog.codinghorror.com/",
         "http://georgestocker.com/", "www.livescore.com/tennis/")

DEFAULT_WORKERS_NO = len(SITES)

PRINTER_LOCK = Lock()
DOWNLOADED_URLS_LOCK = Lock()

DOWNLOADED_URLS_NO = Value('i', 0)
WORKERS_ARGS = []


def download(index):
    """Download the content of the given url

    Args:
        index: the index of the worker
    """
    SITES = ("http://www.hotnews.ro/", "https://www.google.com/",
             "http://stackoverflow.com/", "http://blog.codinghorror.com/",
             "http://georgestocker.com/", "www.livescore.com/tennis/")

    url = SITES[(index - 1) % len(SITES)]

    with PRINTER_LOCK:
        print index, "is downloading", url

    try:
        requests.get(url=url)
    except Exception as ex:
        with PRINTER_LOCK:
            print index, "failed to download", url, ". Error:", ex
        return

    with DOWNLOADED_URLS_LOCK:
        DOWNLOADED_URLS_NO.value += 1


def print_usage():
    """Print the usage for this executable"""
    print "Usage:\n"
    print "./download_with_processes_pool.py [threads_no]"


if __name__ == "__main__":
    """The main function of the executable"""
    if len(sys.argv) > 2:
        print_usage()
        sys.exit(0)

    if len(sys.argv) == 2:
        workers_no = int(sys.argv[1])
    else:
        workers_no = DEFAULT_WORKERS_NO

    for i in range(workers_no):
        WORKERS_ARGS.append(i + 1)

    pool = Pool(processes=workers_no)
    pool.map(download, WORKERS_ARGS)

    print "Downloaded documents:", DOWNLOADED_URLS_NO.value
