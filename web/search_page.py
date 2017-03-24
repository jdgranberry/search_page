from flask import Flask, render_template, request
import configparser
import urllib.parse
import urllib.request
import json
import certifi
from elasticsearch import Elasticsearch



app = Flask(__name__)

NUM_SEARCH_RESULTS = 10

# Pull in the API key to enable search
config = configparser.ConfigParser()
config.read('search_page.env')
api_key = config['Google Search API']['Apikey']
cx = config['Google Search API']['Cx']

# Elasticsearch server
es_host = config['Elasticsearch Server']['Host']
es_port = config['Elasticsearch Server']['Port']
es_user = config['Elasticsearch Server']['User']
es_pass = config['Elasticsearch Server']['Pass']

es = Elasticsearch([es_host], http_auth=(es_user, es_pass), port=es_port)

ES_INDEX = 'song_lyrics'


@app.route('/')
def hello_world():
    return render_template('websearch.html', my_string="Hello World!", my_list=[0, 1, 2, 3, 4, 5])


@app.route("/home")
def home():
    return render_template('websearch.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="Home")


@app.route("/about")
def about():
    return render_template('websearch.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="About")


@app.route("/contact")
def contact():
    return render_template('websearch.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="Contact Us")


# Web Search Functionality #########################################################################
@app.route("/websearch")
def websearch():
    return render_template('websearch.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="Home")


@app.route('/api/websearch', methods=['POST'])
def websearch_post():
    text = request.form['websearch']

    params = {'key': api_key,
              'cx': cx,
              'q': text,
              'num': NUM_SEARCH_RESULTS}

    url = 'https://www.googleapis.com/customsearch/v1?%s' % urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as f:
        json_data = json.loads(f.read().decode('utf-8'))

    return render_template('websearch_results.html',
                           query=text,
                           length=len(json_data['items']),
                           results=json_data['items'])


# Elasticsearch Functionality#######################################################################
@app.route("/elasticsearch")
def elasticsearch():
    return render_template('elasticsearch.html', my_string="Wheeeee!", my_list=[0, 1, 2, 3, 4, 5], title="About")


@app.route("/api/elasticsearch", methods=["POST"])
def elasticsearch_post():
    text = request.form['elasticsearch']

    res = es.search(index=ES_INDEX, size=50, body={"query": {"match_all": {}}})

    results = ""
    for hit in res['hits']['hits']:
        artist = hit['_source']['Artist'].__str__()
        song = hit['_source']['Song'].__str__()
        results += "{}, {}<div>".format(artist, song)
    return results

if __name__ == '__main__':
    app.run()
