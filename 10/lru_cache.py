import logging
import argparse


form1 = logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")
form2 = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")

handler_file = logging.FileHandler("py_log.log")
handler_file.setLevel(logging.DEBUG)
handler_file.setFormatter(form1)

handler_stdout = logging.StreamHandler()
handler_stdout.setLevel(logging.DEBUG)
handler_stdout.setFormatter(form2)

logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler_file)


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.size = 0
        self.data = {}
        logger.info("creating an instance of the LRUCache class \
(limit=%s)", limit)

    def get(self, key):
        is_available = self.update_usage_order(key)
        if is_available:
            logger.debug("get(%s)", key)
        else:
            logger.info("get(%s): key not found", key)
        return self.data.get(key)

    def set(self, key, value):
        if key in self.data:
            self.data.pop(key)
            self.data[key] = value
            logger.debug("set(%s, %s): existing key, \
size = %s", key, value, self.size)
            return
        if self.size >= self.limit:
            key_old = self.long_unused_key()
            self.data.pop(key_old)
            logger.warning("set(%s, %s): new key, key %s deleted, \
size = %s", key, value, key_old, self.size)
            self.size -= 1
        else:
            logger.debug("set(%s, %s): new key, \
size = %s", key, value, self.size + 1)
        self.data[key] = value
        self.size += 1

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, item):
        is_available = self.update_usage_order(item)
        if not is_available:
            logger.error("getitem[%s]: key not found", item)
        else:
            logger.debug("getitem[%s]", item)
        return self.data[item]

    def update_usage_order(self, key):
        if key not in self.data:
            return False
        self.data[key] = self.data.pop(key)
        return True

    def long_unused_key(self):
        return next(iter(self.data))


def run():
    cache = LRUCache(3)

    cache[1] = "one"
    cache[2] = "two"
    cache[3] = "three"

    assert cache[1] == "one"
    assert cache.get(5) is None
    cache[4] = "four"

    cache[1] = "one"
    cache.set(2, "two")
    cache[3] = "three"

    cache[4] = "four"

    cache.set(2, "II")
    cache[3] = "III"

    assert cache.get(3) == "III"

    cache.set(5, "V")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true")
    flag = parser.parse_args().s
    if flag:
        logger.addHandler(handler_stdout)
    run()
