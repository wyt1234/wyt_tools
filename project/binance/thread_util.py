import threading
import time


# 线程安全的quote队列
class QuoteManager:
    def __init__(self):
        self.live_quotes = []
        self.lock = threading.Lock()

    def add_quote(self, quote):
        with self.lock:
            self.live_quotes.append(quote)

    def remove_dead_quotes(self):
        with self.lock:
            self.live_quotes = [quote for quote in self.live_quotes if quote.is_alive()]

    def get_live_quotes(self):
        with self.lock:
            return [quote for quote in self.live_quotes if quote.is_alive()]


# 简单序列生成器
class GlobalIDGenerator:
    def __init__(self):
        self.id = 0
        self.lock = threading.Lock()

    def get_next_id(self):
        with self.lock:
            result = self.id
            self.id += 1
        return result


# 雪花算法序列号生成（时间相关）
class SnowflakeIDGenerator:
    def __init__(self, machine_id=1):
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def get_next_id(self):
        with self.lock:
            timestamp = int(time.time() * 1000)
            if timestamp < self.last_timestamp:
                raise Exception('Clock moved backwards')
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    while timestamp <= self.last_timestamp:
                        timestamp = int(time.time() * 1000)
            else:
                self.sequence = 0
            self.last_timestamp = timestamp
            id = ((timestamp & 0x1FFFFFFFFFF) << 22) | (self.machine_id << 12) | self.sequence
            return id
