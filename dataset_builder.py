import subscription_keys as keys
import requests
import csv

assert keys.azure_bing_news

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
search_term = input('enter search term: ')

headers = {"Ocp-Apim-Subscription-Key" : keys.azure_bing_news}
articles = []

# retrieve 10k articles with text/image/video
print('retrieving articles...')
for i in range(0, 100):
    print(str(i + 1) + ' of 100')
    params  = {"q": search_term, 'freshness': 'Month', 'count': 100, 'offset': i * 100}
    response = requests.get(search_url, headers = headers, params = params)
    response.raise_for_status()
    search_results = response.json()['value']
    for result in search_results:
        article = []
        article.append(result['datePublished'])
        article.append(result['url'])
        article.append(result['name'])
        article.append(result['description'])
        articles.append(article)

with open(str(search_term) + '.csv', 'w', newline = '\n') as file:
    writer = csv.writer(file, delimiter = ',')
    for article in articles:
        writer.writerow(article)
