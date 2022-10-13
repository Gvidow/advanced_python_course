class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.size = 0
        self.data = {}

    def get(self, key):
        self.update_usage_order(key)
        return self.data.get(key)

    def set(self, key, value):
        if key in self.data:
            self.data.pop(key)
            self.data[key] = value
            return
        if self.size >= self.limit:
            self.data.pop(self.long_unused_key())
            self.size -= 1
        self.data[key] = value
        self.size += 1

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, item):
        self.update_usage_order(item)
        return self.data[item]

    def update_usage_order(self, key):
        if key not in self.data:
            return
        self.data[key] = self.data.pop(key)

    def long_unused_key(self):
        return next(iter(self.data))
