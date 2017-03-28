from flask import Flask, render_template, request
import json
import re

from api import elasticsearch as es
from api import websearch as ws

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('search.html')


@app.route("/home")
def home():
    return render_template('search.html', title="Home")


@app.route("/about")
def about():
    return render_template('search.html', title="About")


@app.route("/contact")
def contact():
    return render_template('search.html', title="Contact Us")


@app.route("/search")
def search():
    return render_template('search.html', title="Contact Us")


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['search terms']

    json_data = ws.search(text)

    return render_template('results.html',
                           search_type='web',                           query=text,
                           length=len(json_data['items']),
                           results=json_data['items'])


@app.route("/elasticsearch")
def elasticsearch():
    tagline_ = es.get_info()

    if tagline_ != es.ES_SERVER_DOWN:
        return render_template('elasticsearch.html', title="About")
    else:
        return render_template('ESerror.html')


@app.route("/v1/es", methods=["GET"])
def es_search():
    # Parse search parameters
    args = request.args
    search_type = args['match'] # TODO PREVENT SEARCH_TYPE INJECTION
    query = args['query']


    res = es.search(es.parse_query(search_type, query))
    if search_type == es.ES_SEARCH_ALL:
        return render_template('results.html',
                               search_type='elastic',
                               query=query,
                               length=len(res),
                               results=res)
    elif search_type == es.ES_SEARCH_ID:
        return render_template('single_result.html',
                               artist=res[0]['Artist'],
                               title=res[0]['Song'],
                               year=res[0]['Year'],
                               rank=res[0]['Rank'],
                               lyrics=res[0]['Lyrics'])


@app.route("/api/elasticsearch", methods=["POST"])
def elasticsearch_post():
    text = request.form['elasticsearch']

    query = json.dumps({
        "query": {
            "match": {
                "_all": {
                    "query": text, "operator": "and"
                }
            }
        }
    })

    res = es.search(query)

    if res != es.ES_SERVER_DOWN:
        return render_template('results.html',
                               search_type='elastic',
                               query=text,
                               length=len(res),
                               results=res)
    else:
        return render_template('ESerror.html')

if __name__ == '__main__':
    app.run()
