import azure_keys, requests

assert azure_keys.face_api
base_url = 'https://southcentralus.api.cognitive.microsoft.com/face/v1.0'
key_header = 'Ocp-Apim-Subscription-Key'

def detect(image_url):

    try:
        url = base_url + '/detect'
        headers = {
            key_header: azure_keys.face_api
        }
        params = { 
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses'
        }
        json = {
            'url': image_url
        }
        response = requests.get(url, headers = headers, params = params, json = json)
        response.raise_for_status()
        return response.json()

    except Exception:
        return None
