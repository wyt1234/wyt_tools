from gnews import GNews

google_news = GNews()
pakistan_news = google_news.get_news('Pakistan')
print(pakistan_news[0])
