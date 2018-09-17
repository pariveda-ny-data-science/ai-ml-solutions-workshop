## AI-ML Solutions in Azure Workshop

by [Pariveda NY Data Science](github.com/pariveda-ny-data-science)

---

The content of this workshop is derived from:

[Bing News API Python Quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-news-search/python)

[Cog. Services Text Analytics Python Quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python)

[Cog. Services Computer Vision Python Quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-analyze)

[Cog. Services Face API Python Quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/face/QuickStarts/Python)

In this workshop, we will:
* Collect several thousand article headlines and their source URLs from Bing News about a brand of your choice
* Scrape the full article text and any image links from each URL
* Send the article texts in batches to the various text analytics APIs
* Send the article images to the computer vision and face APIs
* Rearrange the data for analysis and view in Jupyter and/or Power BI

*Python is the primary language of this workshop.*

The modules in this repository WILL NOT FUNCTION without a module containing subscription keys to the various Azure services (not included, to be provided by us at the workshop).

Implementation notes
* A call to the text analytics API is limited to 1000 documents of 5000 characters each, with a maximum request size of 1 MB
* Text analytics API rate limit: 100 calls/min

TODO
* Convert individual Python scripts + this readme into Azure notebook to reduce setup time

Other references
* https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
* https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html
* 