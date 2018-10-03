import azure_keys, requests

assert azure_keys.text_analytics
base_url = 'https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.0'
key_header = 'Ocp-Apim-Subscription-Key'

def sentiment(strings):
    return analyze(strings, 'sentiment')

def key_phrases(strings):
    return analyze(strings, 'keyPhrases')

def entities(strings):
    return analyze(strings, 'entities')

# input: array of strings, max 1000, english only
def analyze(strings, endpoint):
    
    try:
        assert len(strings) <= 1000

        url = base_url + '/' + endpoint
        headers = {
            key_header: azure_keys.text_analytics
        }
        json = { 
            'documents': []
        }
        id = 1
        for string in strings:
            json['documents'].append({
                'id': str(id),
                'language': 'en',
                'text': string
            })
            id += 1
        response = requests.post(url, headers = headers, json = json)
        response.raise_for_status()
        return response.json()

    except Exception:
        return None