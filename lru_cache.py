from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def access_list(self, key: int):
        if key in self.cache:
            self.cache.move_to_end(key)  
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False) 
            self.cache[key] = True

    def display_cache(self):
        print("Cache", list(self.cache.keys()))

if __name__ == "__main__":
    cache_size = 4
    lru_cache = LRUCache(cache_size)
    
    sequence = [1, 2, 3, 4, 1, 2, 5] 
    
    for item in sequence:
        lru_cache.access_list(item)
        lru_cache.display_cache()
