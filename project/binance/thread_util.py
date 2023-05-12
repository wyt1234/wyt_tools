import threading


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
