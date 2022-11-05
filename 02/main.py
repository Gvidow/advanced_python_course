import json


def parse_json(json_str: str, required_fields, keywords, keyword_callback):
    if required_fields is None or keywords is None:
        return
    dictionary = json.loads(json_str)
    for required_field in set(required_fields):
        if required_field in dictionary:
            list_words = dictionary[required_field].split()
            for word in list_words:
                if word in keywords:
                    keyword_callback(word)
