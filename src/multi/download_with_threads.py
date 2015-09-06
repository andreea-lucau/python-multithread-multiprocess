"""This is an example of using multiple threads to download several websites."""
#!/usr/bin/env python

import requests
import sys
from threading import Thread, Lock

SITES = ("http://www.hotnews.ro/", "https://www.google.com/",
         "http://stackoverflow.com/", "http://blog.codinghorror.com/",
         "http://georgestocker.com/", "www.livescore.com/tennis/")

DEFAULT_WORKERS_NO = len(SITES)

PRINTER_LOCK = Lock()
COUNTER_LOCK = Lock()

DOWNLOADED_URLS_NO = 0


def download(index, url):
    """Download the content of the given url

    Args:
        index: the index of the thread doing the work
        url: the url to download
    """
    with PRINTER_LOCK:
        print index, "is downloading", url

    try:
        requests.get(url=url)
    except Exception as ex:
        with PRINTER_LOCK:
            print index, "failed to download", url, ". Error:", ex
        return

    with COUNTER_LOCK:
        global DOWNLOADED_URLS_NO
        DOWNLOADED_URLS_NO += 1


def print_usage():
    """Print the usage for this executable"""
    print "Usage:\n"
    print "./download_with_threads.py [threads_no]"


def main():
    """The main function of the executable"""
    if len(sys.argv) > 2:
        print_usage()
        return

    if len(sys.argv) == 2:
        threads_no = int(sys.argv[1])
    else:
        threads_no = DEFAULT_WORKERS_NO

    workers = []
    for i in range(threads_no):
        worker = Thread(target=download, args=(i + 1, SITES[i % len(SITES)], ))
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    print "Downloaded documents:", DOWNLOADED_URLS_NO

if __name__ == "__main__":
    main()
