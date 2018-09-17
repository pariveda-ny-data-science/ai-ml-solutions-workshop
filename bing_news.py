import azure_keys, requests

assert azure_keys.bing_news
base_url = 'https://api.cognitive.microsoft.com/bing/v7.0/news'
key_header = 'Ocp-Apim-Subscription-Key'

def search(query, count = 10, offset = 0):

    try:
        url = base_url + '/search'
        headers = {
            key_header: azure_keys.bing_news
        }
        params = { 
            'q': query, 
            'count': count, 
            'offset': offset 
        }
        response = requests.get(url, headers = headers, params = params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None
        