import dataset_builder, json

brand = 'microsoft'

articles = dataset_builder.get_articles(brand, 100)
dataset_builder.add_headline_sentiments(articles)
dataset_builder.add_text_key_phrases(articles)
dataset_builder.add_text_entities(articles)
dataset_builder.add_image_analysis(articles)
dataset_builder.add_image_faces(articles)

dataset_builder.dump(brand, articles)

dataset_builder.flatten(brand, articles)
