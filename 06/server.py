import argparse
import socket
import queue
import threading
import string
from collections import Counter
from urllib.request import urlopen
from bs4 import BeautifulSoup


class CustomCounter:
    def __init__(self):
        self.total_processed = 0
        self.processes_with_errors = 0

    def add(self):
        self.total_processed += 1

    def add_err(self):
        self.processes_with_errors += 1

    def __str__(self):
        return f"Всего обработано {self.total_processed}," \
               f" из них с ошибками {self.processes_with_errors}."


def word_counter(text, top):
    for char in string.punctuation + string.digits:
        text = text.replace(char, " ")
    counter = Counter(text.split())
    return dict(counter.most_common(top))


def parse_html(data, top):
    soup = BeautifulSoup(data, 'lxml')
    text = ""
    for tag in soup.recursiveChildGenerator():
        if tag.name == "body":
            text = tag.text
            break
    return word_counter(text, top)


def fetch(que, stat, lock, top, cou):
    while True:
        url = que.get()
        if url is None:
            break
        try:
            with urlopen(url) as response:
                res = parse_html(response.read().decode(), top)
                stat.put((url, res))
        except Exception as err:
            lock.acquire()
            cou.add_err()
            stat.put((url, err))
            lock.release()
        finally:
            lock.acquire()
            cou.add()
            lock.release()


def output(stat, conn, cou):
    while True:
        res = stat.get()
        if res is None:
            break
        conn.send((res[0] + " " + str(res[1]) + "\n").encode())
        print(cou)


def main(count_thread, top):
    que = queue.Queue(count_thread)
    stat = queue.Queue(count_thread)
    lock = threading.Lock()
    cou = CustomCounter()
    threads = [threading.Thread(target=fetch, args=(que, stat, lock, top, cou))
               for _ in range(count_thread)]
    for i in range(count_thread):
        threads[i].start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 8080))
    sock.listen()

    conn, _ = sock.accept()
    thread_output = threading.Thread(target=output, args=(stat, conn, cou))
    thread_output.start()
    while conn:
        data = conn.recv(1024).decode("utf-8").strip()
        if data == "exit":
            break
        for url in data.split("\n"):
            que.put(url)

    conn.close()

    for _ in range(count_thread):
        que.put(None)
    for i in range(count_thread):
        threads[i].join()
    stat.put(None)
    thread_output.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", type=int, default=1)
    parser.add_argument("-k", type=int, default=1)
    args = parser.parse_args()
    main(args.w, args.k)
