import azure_keys, requests

assert azure_keys.computer_vision
base_url = 'https://southcentralus.api.cognitive.microsoft.com/vision/v2.0'
key_header = 'Ocp-Apim-Subscription-Key'

def analyze(image_url):

    try:
        url = base_url + '/analyze'
        headers = {
            key_header: azure_keys.computer_vision
        }
        params = { 
            'visualFeatures': 'Categories,Tags,Description,Faces,ImageType,Color,Adult',
            'details': 'Celebrities,Landmarks'
        }
        json = {
            'url': image_url
        }
        response = requests.post(url, headers = headers, params = params, json = json)
        response.raise_for_status()
        return response.json()

    except Exception:
        return None
