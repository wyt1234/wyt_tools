
from pygooglenews import GoogleNews
gn = GoogleNews()
top = gn.top_news()
business = gn.topic_headlines('business')
headquaters = gn.geo_headlines('San Fran')
