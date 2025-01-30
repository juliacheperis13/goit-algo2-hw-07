import random
import time
from functools import lru_cache
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def invalidate(self, index):
        keys_to_remove = [
            key for key in self.cache if index >= key[0] and index <= key[1]
        ]
        for key in keys_to_remove:
            del self.cache[key]


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, L, R, cache):
    cached_result = cache.get((L, R))
    if cached_result is not None:
        return cached_result
    result = sum(array[L : R + 1])
    cache.put((L, R), result)
    return result


def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate(index)


def generate_test_data(N, Q):
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.random() < 0.7:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 1000)
            queries.append(("Update", index, value))
    return array, queries


def run_tests():
    N, Q = 100000, 50000
    array, queries = generate_test_data(N, Q)
    cache = LRUCache(1000)

    # Без кешу
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    no_cache_time = time.time() - start

    # З кешем
    array, queries = generate_test_data(N, Q)  # Перегенеруємо дані
    cache = LRUCache(1000)
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array, query[1], query[2], cache)
        else:
            update_with_cache(array, query[1], query[2], cache)
    cache_time = time.time() - start

    print(f"Час виконання без кешу: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")


# Час виконання без кешу: 6.96 секунд
# Час виконання з LRU-кешем: 7.15 секунд

if __name__ == "__main__":
    run_tests()
