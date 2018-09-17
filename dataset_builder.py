import bing_news, time, random

MAX_COUNT = 100
MAX_API_ERRORS = 5

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
    return articles

def add_text_key_phrases(articles):
    return articles

def add_text_entities(articles):
    return articles

def analyze_images(articles):
    return articles
    
def detect_image_faces(articles):
    return articles
