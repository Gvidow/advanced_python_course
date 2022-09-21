import json


def parse_json(json_str: str, required_fields, keywords, keyword_callback):
    if required_fields is None or keywords is None:
        return
    dictionary = json.loads(json_str)
    for k, w in dictionary.items():
        if k in required_fields:
            list_words = w.split()
            for word in list_words:
                if word in keywords:
                    keyword_callback(word)
