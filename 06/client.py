import socket
import sys
import threading
import queue


def send_url(que, conn, lock_send, lock_read):
    while True:
        url = que.get()
        if url is None:
            break
        lock_send.acquire()
        conn.send((url + "\n").encode())
        lock_send.release()
        lock_read.acquire()
        print(conn.recv(1024).decode("utf-8"))
        lock_read.release()


def main(count_thread, reader):
    lock_send = threading.Lock()
    lock_read = threading.Lock()
    que = queue.Queue(count_thread)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("127.0.0.1", 8080))
    cou = 0
    threads = [threading.Thread(target=send_url,
                                args=(que, conn, lock_send, lock_read))
               for _ in range(count_thread)]
    for i in range(count_thread):
        threads[i].start()
    with open(reader, "r", encoding="utf-8") as file:
        iterator = iter(file)
        while True:
            cou += 1
            try:
                url = next(iterator).strip()
                que.put(url)
            except StopIteration:
                break
    for _ in range(count_thread):
        que.put(None)
    for i in range(count_thread):
        threads[i].join()
    conn.send(b"exit\n")
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(int(sys.argv[1]), sys.argv[2])
