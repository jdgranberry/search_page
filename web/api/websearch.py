import configparser
import urllib
import json

NUM_SEARCH_RESULTS = 10         # Valid values are integers between 1 and 10, inclusive.

# Pull in the API key to enable search
config = configparser.ConfigParser()
config.read('search_page.env')
api_key = config['Google Search API']['Apikey']
cx = config['Google Search API']['Cx']


def search(query):

    params = {'key': api_key,
              'cx': cx,
              'q': query,
              'num': NUM_SEARCH_RESULTS}

    url = 'https://www.googleapis.com/customsearch/v1?%s' % urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as f:
        json_data = json.loads(f.read().decode('utf-8'))


    return json_data
