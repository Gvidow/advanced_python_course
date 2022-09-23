import json


def parse_json(json_str: str, required_fields, keywords, keyword_callback):
    if required_fields is None or keywords is None:
        return
    dictionary = json.loads(json_str)
    for key_word, words in dictionary.items():
        if key_word in required_fields:
            list_words = words.split()
            for word in list_words:
                if word in keywords:
                    keyword_callback(word)
