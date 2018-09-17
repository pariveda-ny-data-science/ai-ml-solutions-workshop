import bing_news, time, random, text_analytics

MAX_COUNT = 100
MAX_API_ERRORS = 5
TEXT_BATCH_SIZE = 1000

def get_articles(brand, num_articles):

    articles = []
    est_matches = MAX_COUNT
    errors = 0

    print('searching for ' + brand + ' news...')
    while len(articles) < num_articles and len(articles) + MAX_COUNT <= est_matches:

        news = bing_news.search(brand, MAX_COUNT, len(articles))
        
        try:
            assert news and news['totalEstimatedMatches'] and news['value']

            if est_matches == MAX_COUNT:
                est_matches = news['totalEstimatedMatches']

            for item in news['value']:
                articles.append(item)

        except Exception:
            errors += 1
            print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
            if errors >= MAX_API_ERRORS:
                print('hit max errors, stopping search for ' + brand + 'news.')
                return articles
            seconds_to_wait = random.randint(1, 10)
            print('waiting ' + str(seconds_to_wait) + ' seconds...')
            time.sleep(seconds_to_wait)

        print('retrieved ' + str(len(articles)) + ' of ' + str(num_articles) + ' requested articles.')

    return articles

def add_headline_sentiment(articles):

    num_slices = int(len(articles) / TEXT_BATCH_SIZE) + 1
    errors = 0

    print('starting headline sentiment analysis...')
    for i in range(0, num_slices):

        articles_slice = articles[i * TEXT_BATCH_SIZE : i * TEXT_BATCH_SIZE + TEXT_BATCH_SIZE]
        strings = []

        for article in articles_slice:
            if 'name' in article:
                strings.append(article['name'])   
            else:
                strings.append('')

        response = text_analytics.sentiment(strings)
        num_added = 0

        try:
            assert response and response['documents']
            documents = response['documents']
            assert len(documents) == len(articles_slice)

            for j in range(0, len(documents)):
                articles_slice[j]['headlineSentiment'] = documents[j]['score']
                num_added += 1

        except Exception:
            errors += 1
            print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
            if errors >= MAX_API_ERRORS:
                print('hit max errors, stopping sentiment analysis.')
                return articles
            seconds_to_wait = random.randint(1, 10)
            print('waiting ' + str(seconds_to_wait) + ' seconds...')
            time.sleep(seconds_to_wait)

        print('added sentiment for ' + str(num_added) + ' headlines.')

    return articles

def add_text_key_phrases(articles):
        
    num_slices = int(len(articles) / TEXT_BATCH_SIZE) + 1
    errors = 0

    print('starting key prhase analysis...')
    for i in range(0, num_slices):

        articles_slice = articles[i * TEXT_BATCH_SIZE : i * TEXT_BATCH_SIZE + TEXT_BATCH_SIZE]
        strings = []

        for article in articles_slice:
            if 'description' in article:
                strings.append(article['description'])   
            else:
                strings.append('')

        response = text_analytics.key_phrases(strings)
        num_added = 0

        try:
            assert response and response['documents']
            documents = response['documents']
            assert len(documents) == len(articles_slice)

            for j in range(0, len(documents)):
                articles_slice[j]['textKeyPhrases'] = documents[j]['keyPhrases']
                num_added += 1

        except Exception:
            errors += 1
            print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
            if errors >= MAX_API_ERRORS:
                print('hit max errors, stopping key phrase analysis.')
                return articles
            seconds_to_wait = random.randint(1, 10)
            print('waiting ' + str(seconds_to_wait) + ' seconds...')
            time.sleep(seconds_to_wait)

        print('added key phrases for ' + str(num_added) + ' articles.')
    
    return articles

def add_text_entities(articles):

    num_slices = int(len(articles) / TEXT_BATCH_SIZE) + 1
    errors = 0

    print('starting entity extraction...')
    for i in range(0, num_slices):

        articles_slice = articles[i * TEXT_BATCH_SIZE : i * TEXT_BATCH_SIZE + TEXT_BATCH_SIZE]
        strings = []

        for article in articles_slice:
            if 'description' in article:
                strings.append(article['description'])   
            else:
                strings.append('')

        response = text_analytics.entities(strings)
        num_added = 0

        try:
            assert response and response['documents']
            documents = response['documents']
            assert len(documents) == len(articles_slice)

            for j in range(0, len(documents)):
                articles_slice[j]['textEntities'] = documents[j]['entities']
                num_added += 1

        except Exception:
            errors += 1
            print('error occured. (' + str(errors) + ' of ' + str(MAX_API_ERRORS) + ' allowed.)')
            if errors >= MAX_API_ERRORS:
                print('hit max errors, stopping entity extraction.')
                return articles
            seconds_to_wait = random.randint(1, 10)
            print('waiting ' + str(seconds_to_wait) + ' seconds...')
            time.sleep(seconds_to_wait)

        print('added entities for ' + str(num_added) + ' articles.')

    return articles

def analyze_images(articles):
    return articles
    
def detect_image_faces(articles):
    return articles
