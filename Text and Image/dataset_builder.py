import bing_news, time, random, text_analytics, computer_vision, face_api, csv

NEWS_MAX_COUNT = 100
MAX_API_ERRORS = 3
TEXT_BATCH_SIZE = 1000

def get_articles(brand, num_articles):

    assert brand != ''

    print('searching for "' + brand + '" news...')
    articles = []
    count = NEWS_MAX_COUNT
    est_matches = None
    errors = 0
    while len(articles) < num_articles and (est_matches is None or len(articles) < est_matches):

        if num_articles < count:
            count = num_articles

        news = bing_news.search(brand, count, len(articles))
        
        try:
            assert news and news['totalEstimatedMatches'] and news['value']

            if est_matches is None:
                est_matches = news['totalEstimatedMatches']

            for item in news['value']:
                articles.append(item)

            print('retrieved ' + str(len(articles)) + ' of ' + str(num_articles) + ' requested articles.')

        except Exception:
            errors += 1
            print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
            if errors >= MAX_API_ERRORS:
                print('hit max errors, stopping search for ' + brand + 'news.')
                return articles
            seconds_to_wait = random.randint(1, 10)
            print('waiting ' + str(seconds_to_wait) + ' seconds...')
            time.sleep(seconds_to_wait)

    return articles

def add_headline_sentiments(articles):
    return add_text_analysis(articles, 'sentiment', 'name', 'headlineSentiment', 'score')

def add_text_key_phrases(articles):
    return add_text_analysis(articles, 'keyPhrases', 'description', 'textKeyPhrases', 'keyPhrases')

def add_text_entities(articles):
    return add_text_analysis(articles, 'entities', 'description', 'textEntities', 'entities')

def add_image_analysis(articles):

    print('starting image analysis...')
    i = 0
    analyzed = 0
    errors = 0
    while i < len(articles):

        article = articles[i]

        if 'image' in article and 'contentUrl' in article['image']:
            
            response = computer_vision.analyze(article['image']['contentUrl'])

            try:
                assert response and type(response) is dict
                article['image']['analysis'] = response
                analyzed += 1
                i += 1
                errors = 0
                print('image analyzed. waiting 3 seconds...')
                time.sleep(3)

            except Exception:
                errors += 1
                # print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
                if errors >= MAX_API_ERRORS:
                    print('hit max errors, skipping image.')
                    i += 1
                    errors = 0
                    continue
                seconds_to_wait = 1
                # print('waiting ' + str(seconds_to_wait) + ' seconds...')
                time.sleep(seconds_to_wait)

        else:
            i += 1

    print('analyzed ' + str(analyzed) + ' of ' + str(len(articles)) + ' articles. (articles with images.)')

    return articles

def add_image_faces(articles):

    print('starting image face detection ...')
    i = 0
    analyzed = 0
    faces = 0
    while i < len(articles):

        article = articles[i]
        errors = 0

        if 'image' in article and 'contentUrl' in article['image']:
            
            response = face_api.detect(article['image']['contentUrl'])

            try:
                assert type(response) is list
                article['image']['faces'] = response
                analyzed += 1
                faces += len(response)
                i += 1
                print('.')

            except Exception:
                errors += 1
                # print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
                if errors >= MAX_API_ERRORS:
                    print('hit max errors, skipping image.')
                    i += 1
                    continue
                seconds_to_wait = 1
                # print('waiting ' + str(seconds_to_wait) + ' seconds...')
                time.sleep(seconds_to_wait)

        else:
            i += 1

    print('analyzed ' + str(analyzed) + ' of ' + str(len(articles)) + ' articles. (articles with images.)')
    print('detected ' + str(faces) + ' faces in ' + str(analyzed) + ' articles.')

    return articles

def add_text_analysis(articles, endpoint, article_text_key, article_new_key, response_key):

    print('starting text analysis (endpoint: ' + endpoint + ')...')
    i = 0
    num_batches = int(len(articles) / TEXT_BATCH_SIZE) + 1
    analyzed = 0
    errors = 0
    while i < num_batches:

        batch = articles[i * TEXT_BATCH_SIZE : (i + 1) * TEXT_BATCH_SIZE]
        string_batch = []

        for article in batch:
            if article_text_key in article:
                string_batch.append(article[article_text_key])   
            else:
                string_batch.append('')

        response = text_analytics.analyze(string_batch, endpoint)

        try:
            assert response and response['documents']
            documents = response['documents']
            assert len(documents) == len(batch)

            for j in range(0, len(documents)):
                assert response_key in documents[j]

            for j in range(0, len(documents)):
                batch[j][article_new_key] = documents[j][response_key]
            analyzed += len(documents)
            i += 1

            print('analyzed ' + str(analyzed) + ' of ' + str(len(articles)) + ' articles.')

        except Exception:
            errors += 1
            print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
            if errors >= MAX_API_ERRORS:
                print('hit max errors, stopping text analysis.')
                return articles
            seconds_to_wait = random.randint(1, 10)
            print('waiting ' + str(seconds_to_wait) + ' seconds...')
            time.sleep(seconds_to_wait)

    return articles

def flatten(brand, articles):
    with open(brand.replace(' ', '-') + '.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        headers = ['headline', 'headlineSentiment', 'text', 'textKeyPhrases', 'textEntities', 'imageUrl']
        headers.extend(['imageAdultScore', 'imageRacyScore', 'imageCategories', 'imageColors', 'imageCaptions'])
        headers.extend(['imageTags', 'imageFaceCount', 'imageFaceAge'])
        writer.writerow(headers)
        for article in articles:
            try:
                row = []
                row.append(article['name'])
                row.append(str(article['headlineSentiment']))
                row.append(article['description'])
                key_phrases = ''
                for i in range(0, len(article['textKeyPhrases'])):
                    if i != 0:
                        key_phrases += ','
                    key_phrases += article['textKeyPhrases'][i]
                row.append(key_phrases)
                entities = ''
                for i in range(0, len(article['textEntities'])):
                    if i != 0:
                        entities += ','
                    entities += article['textEntities'][i]['name']
                row.append(entities)
                if 'image' in article:
                    row.append(article['image']['contentUrl'])
                    row.append(article['image']['analysis']['adult']['adultScore'])
                    row.append(article['image']['analysis']['adult']['racyScore'])
                    categories = ''
                    for i in range(0, len(article['image']['analysis']['categories'])):
                        if i != 0:
                            categories += ','
                        categories += article['image']['analysis']['categories'][i]['name']
                    row.append(categories)
                    colors = ''
                    for i in range(0, len(article['image']['analysis']['color']['dominantColors'])):
                        if i != 0:
                            colors += ','
                        colors += article['image']['analysis']['color']['dominantColors'][i]
                    row.append(colors)
                    captions = ''
                    for i in range(0, len(article['image']['analysis']['description']['captions'])):
                        if i != 0:
                            captions += ','
                        captions += article['image']['analysis']['description']['captions'][i]['text']
                    row.append(captions)
                    tags = ''
                    for i in range(0, len(article['image']['analysis']['description']['tags'])):
                        if i != 0:
                            tags += ','
                        tags += article['image']['analysis']['description']['tags'][i]
                    row.append(tags)
                    row.append(str(len(article['image']['faces'])))
                    age = 0
                    for i in range(0, len(article['image']['faces'])):
                        age += article['image']['faces'][i]['faceAttributes']['age']
                    age = age / len(article['image']['faces'])
                    row.append(age)
                else:
                    for i in range(0, 9):
                        row.append('')
                writer.writerow(row)
            except Exception:
                continue
