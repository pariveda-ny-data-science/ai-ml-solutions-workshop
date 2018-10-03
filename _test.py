import dataset_builder, json

brand = 'star trek'

articles = dataset_builder.get_articles(brand, 1)
dataset_builder.add_headline_sentiments(articles)
dataset_builder.add_text_key_phrases(articles)
dataset_builder.add_text_entities(articles)
dataset_builder.add_image_analysis(articles)
dataset_builder.add_image_faces(articles)

with open(str(brand.replace(' ', '-')) + '.json', 'w') as json_file:
    json.dump(articles, json_file, indent = 4, sort_keys = True)
