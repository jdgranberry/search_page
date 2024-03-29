from elasticsearch import Elasticsearch, exceptions
import configparser
import json

config = configparser.ConfigParser()
config.read('search_page.env')
es_host = config['Elasticsearch Server']['Host']
es_port = config['Elasticsearch Server']['Port']
es_user = config['Elasticsearch Server']['User']
es_pass = config['Elasticsearch Server']['Pass']

ES_INDEX = 'song_lyrics'

ES_SERVER_UP = "ES_SERVER_UP"
ES_SERVER_DOWN = "ES_SERVER_DOWN"
ES_SERVER_SEARCH_ERROR = "ES_SERVER_SEARCH_ERROR"
ES_SEARCH_ALL = '_all'
ES_SEARCH_ID = '_id'

es = Elasticsearch([es_host], http_auth=(es_user, es_pass), port=es_port)


def get_status():
    try:
        # Try a simple request to the server
        es.info()
        return ES_SERVER_UP
    except exceptions.ConnectionError:
        return ES_SERVER_DOWN


def parse_query(search_type, text):
    search_type_ = search_type

    if search_type == ES_SEARCH_ALL:
        text_ = {"query": text, "operator": "and"}
    elif search_type == ES_SEARCH_ID:
        text_ = {"query": text}
    else:
        search_type_ = ES_SEARCH_ALL
        text_ = {"query": text, "operator": "and"}

    json_query = json.dumps({
        "query": {
            "match": {
                search_type_: text_
            }
        }
    })

    return json_query


def search(json_query):
    try:
        res = es.search(index=ES_INDEX, size=50, body=json_query)

        results = list()
        for hit in res['hits']['hits']:
            results.append({'Artist': hit['_source']['Artist'],
                            'Song': hit['_source']['Song'],
                            'Year': hit['_source']['Year'],
                            'Rank': hit['_source']['Rank'],
                            'Lyrics': hit['_source']['Lyrics'],
                            'Id': hit['_id']})
        return results

    except exceptions.ConnectionError:
        return ES_SERVER_DOWN
