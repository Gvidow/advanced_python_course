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
        self.data = 0

    def add(self):
        self.data += 1

    def get(self):
        return self.data


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
                print(cou.get())
                res = parse_html(response.read().decode(), top)
                lock.acquire()
                cou.add()
                lock.release()
                stat.put(res)
                print(cou.get())
        except Exception as err:
            print(url)
            print(err)


def output(stat, conn, cou):
    while True:
        res = stat.get()
        if res is None:
            break
        conn.send((str(res) + "\n").encode())
        print("Количество обработанных запросов:", cou.get())


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
    sock.bind(("127.0.0.1", 8081))
    sock.listen()

    conn, _ = sock.accept()
    thread_output = threading.Thread(target=output, args=(stat, conn, cou))
    thread_output.start()
    while conn:
        data = conn.recv(1024).decode("utf-8").strip()
        print(f"'{data}'")
        if data == "exit":
            break
        que.put(data)

    conn.close()

    for _ in range(count_thread):
        que.put(None)
    stat.put(None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", type=int, default=1)
    parser.add_argument("-k", type=int, default=1)
    args = parser.parse_args()
    main(args.w, args.k)
