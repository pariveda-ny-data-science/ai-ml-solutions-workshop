import subscription_keys as keys
import requests
from IPython.display import HTML

assert keys.azure_bing_news

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
search_term = "Microsoft"

headers = {"Ocp-Apim-Subscription-Key" : keys.azure_bing_news}
params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

descriptions = [article["description"] for article in search_results["value"]]

rows = "\n".join(["<tr><td>{0}</td></tr>".format(desc) for desc in descriptions])
HTML("<table>"+rows+"</table>")