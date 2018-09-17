import dataset_builder, text_analytics

articles = dataset_builder.get_articles('microsoft', 50)
titles = []
for article in articles:
    titles.append(article['name'])
response = text_analytics.sentiment(titles)
print(response)