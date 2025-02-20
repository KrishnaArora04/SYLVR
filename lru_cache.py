from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key) 
            return self.cache[key]
        return -1

    def put(self, key: int, value: int):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False) 

        self.cache[key] = value

    def display(self):
        print("Cache:", list(self.cache.items()))

    def size(self) -> int:
        return len(self.cache)


if __name__ == "__main__":
    cache = LRUCache(4)

    operations = [(1, 10), (2, 20), (3, 30), (4, 40), (1, 15), (2, 25), (5, 50)]

    for key, value in operations:
        cache.put(key, value)
        cache.display()

    print("Fetching key 3:", cache.get(3)) 
    print("Fetching key 6:", cache.get(6)) 
    print("Cache size:", cache.size())
    
