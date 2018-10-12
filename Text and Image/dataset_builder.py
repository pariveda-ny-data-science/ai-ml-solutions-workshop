import bing_news, time, random, text_analytics, computer_vision, face_api, os, json, csv

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

    return articles[:num_articles]

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
            # time.sleep(3)

            try:
                assert response and type(response) is dict
                article['image']['analysis'] = response
                analyzed += 1
                i += 1
                errors = 0
                print('image analyzed.')

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
            # time.sleep(3)

            try:
                assert type(response) is list
                article['image']['faces'] = response
                analyzed += 1
                faces += len(response)
                i += 1
                print('image analyzed.')

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

def dump(brand, articles):

    brand_folder = os.getcwd() + '/output/' + brand.lower().replace(' ', '-')
    if not os.path.exists(brand_folder):
        os.makedirs(brand_folder)

    with open(brand_folder + '/articles.json', 'w') as json_file:
        json.dump(articles, json_file, indent = 4, sort_keys = True)

def flatten(brand, articles):

    brand_folder = os.getcwd() + '/output/' + brand.lower().replace(' ', '-')
    if not os.path.exists(brand_folder):
        os.makedirs(brand_folder)

    csv_articles = []
    csv_articles.append(['articleLink', 'headline', 'headlineSentiment', 'textSnippet'])

    entities = []
    entities.append(['articleLink', 'entity', 'wikiLink'])

    key_phrases = []
    key_phrases.append(['articleLink', 'phrase'])

    images = []
    images_header = ['articleLink', 'imageLink', 'adultScore', 'isRacyContent', 'isAdultContent', 'racyScore']
    images_header.extend(['accentColor', 'dominantColorBackground', 'dominantColorForeground', 'isBwImg'])
    images_header.extend(['clipArtType', 'lineDrawingType', 'format', 'height', 'width'])
    images.append(images_header)

    image_categories = []
    image_categories.append(['articleLink', 'imageLink', 'category', 'score'])

    image_colors = []
    image_colors.append(['articleLink', 'imageLink', 'color'])

    image_desc_tags = []
    image_desc_tags.append(['articleLink', 'imageLink', 'tag'])

    image_desc_captions = []
    image_desc_captions.append(['articleLink', 'imageLink', 'caption', 'confidence'])

    image_tags = []
    image_tags.append(['articleLink', 'imageLink', 'tag', 'confidence'])

    image_faces = []
    faces_header = ['articleLink', 'imageLink', 'accessories', 'age', 'anger', 'contempt', 'disgust']
    faces_header.extend(['fear', 'happiness', 'neutral', 'sadness', 'surprise', 'beard', 'mustache', 'sideburns'])
    faces_header.extend(['gender', 'glasses', 'bald', 'hairColor', 'makeup', 'smile'])
    image_faces.append(faces_header)

    for article in articles:

        try:
            csv_articles.append([article['url'], article['name'], article['headlineSentiment'], article['description']])
        except Exception:
            pass

        try:
            for entity in article['textEntities']:
                entities.append([article['url'], entity['name'], entity['wikipediaUrl']])
        except Exception:
            pass

        try:
            for phrase in article['textKeyPhrases']:
                key_phrases.append([article['url'], phrase])
        except Exception:
            pass

        try:
            image = article['image']
            adult = image['analysis']['adult']
            color = image['analysis']['color']
            imageType = image['analysis']['imageType']
            metadata = image['analysis']['metadata']
            row = [article['url'], image['contentUrl'], adult['adultScore'], adult['isRacyContent'], adult['isAdultContent'], adult['racyScore']]
            row.extend([color['accentColor'], color['dominantColorBackground'], color['dominantColorForeground'], color['isBwImg']])
            row.extend([imageType['clipArtType'], imageType['lineDrawingType'], metadata['format'], metadata['height'], metadata['width']])
            images.append(row)
        except Exception:
            pass

        try:
            image = article['image']
            for category in image['analysis']['categories']:
                image_categories.append([article['url'], image['contentUrl'], category['name'], category['score']])
        except Exception:
            pass

        try:
            image = article['image']
            for color in image['analysis']['color']['dominantColors']:
                image_colors.append([article['url'], image['contentUrl'], color])
        except Exception:
            pass

        try:
            image = article['image']
            description = image['analysis']['description']
            for tag in description['tags']:
                image_desc_tags.append([article['url'], image['contentUrl'], tag])
        except Exception:
            pass

        try:
            image = article['image']
            description = image['analysis']['description']
            for caption in description['captions']:
                image_desc_captions.append([article['url'], image['contentUrl'], caption['text'], caption['confidence']])
        except Exception:
            pass

        try:
            image = article['image']
            tags = image['analysis']['tags']
            for tag in tags:
                image_tags.append([article['url'], image['contentUrl'], tag['name'], tag['confidence']])
        except Exception:
            pass

        try:
            image = article['image']
            for face in image['faces']:
                faceAttributes = face['faceAttributes']
                emotion = faceAttributes['emotion']
                facialHair = faceAttributes['facialHair']
                hair = faceAttributes['hair']
                makeup = faceAttributes['makeup']
                row = [article['url'], image['contentUrl'], len(faceAttributes['accessories']) > 0, faceAttributes['age'], emotion['anger'], emotion['contempt'], emotion['disgust']]
                row.extend([emotion['fear'], emotion['happiness'], emotion['neutral'], emotion['sadness'], emotion['surprise'], facialHair['beard'], facialHair['moustache'], facialHair['sideburns']])
                row.extend([faceAttributes['gender'], faceAttributes['glasses'], hair['bald'], hair['hairColor'][0]['color'], makeup['eyeMakeup'] or makeup['lipMakeup'], faceAttributes['smile']])
                image_faces.append(row)
        except Exception:
            pass

    with open(brand_folder + '/articles.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in csv_articles:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/entities.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in entities:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/key-phrases.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in key_phrases:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/images.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in images:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/image-categories.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in image_categories:
            writer.writerow(category)

    with open(brand_folder + '/image-colors.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in image_colors:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/image-desc-tags.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in image_desc_tags:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/image-desc-captions.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in image_desc_captions:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/image-tags.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in image_tags:
            try:
                writer.writerow(row)
            except Exception:
                continue

    with open(brand_folder + '/image-faces.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in image_faces:
            try:
                writer.writerow(row)
            except Exception:
                continue
