from random import randint, choice
import factory


class TestData:
    def __init__(self, list_words):
        self.unique_words = list(set(list_words))
        self.count_unique_words = len(self.unique_words)
        self.expected_count_calls = 0
        self.call_args_set = set()
        self.json_dict = {}
        self.required_fields = []
        self.keywords = []
        if self.count_unique_words != 0:
            self.build_json_dict()
        self.parse_dict()

    def build_json_dict(self):
        count_required_fields = randint(0, self.count_unique_words)
        count_keywords = randint(0, self.count_unique_words
                                 - count_required_fields)
        self.required_fields = self.unique_words[:count_required_fields]
        self.keywords = self.unique_words[
                        count_required_fields:
                        count_required_fields + count_keywords]
        remaining_words = self.unique_words[
                          count_required_fields + count_keywords:]

        if count_required_fields != 0:
            for _ in range(randint(0, 50)):
                required_field = choice(self.required_fields)
                if required_field in self.json_dict:
                    for _ in range(randint(0, 100)):
                        group = randint(1, 2)
                        if group == 1 and count_keywords != 0:
                            keyword = choice(self.keywords)
                            self.json_dict[required_field].append(keyword)
                            self.call_args_set.add(keyword)
                            self.expected_count_calls += 1
                        else:
                            self.json_dict[required_field].append(
                                choice(self.required_fields + remaining_words))
                else:
                    self.json_dict[required_field] = []

        if count_required_fields != self.count_unique_words:
            for _ in range(50):
                keyword = choice(self.keywords + remaining_words)
                if keyword in self.json_dict:
                    for _ in range(randint(0, 100)):
                        self.json_dict[keyword].append(
                            choice(self.unique_words))
                else:
                    self.json_dict[keyword] = []

    def parse_dict(self):
        dictionary = self.json_dict.copy()
        for key in dictionary:
            dictionary[key] = " ".join(dictionary[key])
        json_string = str(dictionary)
        return json_string.replace("'", "\"")


class TestDataFactory(factory.Factory):
    class Meta:
        model = TestData

    list_words = factory.List([factory.Faker("word")
                               for _ in range(randint(0, 500))])
