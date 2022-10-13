def filter_file(reader, words):
    words = list(map(lambda x: x.lower(), words))
    with open(reader, "r", encoding="utf-8") as file:
        iterator = iter(file)
        try:
            while True:
                string = next(iterator).strip()
                strings = string.lower().split()
                for word in words:
                    if word in strings:
                        yield string
                        break
        except StopIteration:
            pass
