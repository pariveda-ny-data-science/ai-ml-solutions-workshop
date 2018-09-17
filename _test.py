import dataset_builder, text_analytics

articles = dataset_builder.get_articles('microsoft', 50)

dataset_builder.add_headline_sentiment(articles)
dataset_builder.add_text_key_phrases(articles)
dataset_builder.add_text_entities(articles)

# titles = []
# for article in articles:
#     titles.append(article['name'])
# response = text_analytics.sentiment(titles)