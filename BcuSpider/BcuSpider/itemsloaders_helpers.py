class IncrementId:
    counter = 0

    @classmethod
    def increment_on_call(cls, y=1):
        cls.counter += y
        return cls.counter

    @classmethod
    def reset_counter(cls):
        cls.counter = 0


def remove_last_element_from_url(url):
    partition = url.rpartition("/")
    return partition[0] + partition[1]
