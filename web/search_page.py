from flask import Flask, render_template, request, Markup
import markdown
import json

from api import elasticsearch as es
from api import websearch as ws

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route("/home")
def home():
    return render_template('index.html', title="Home")


@app.route("/about")
def about():
    import os

    # Load `../README.md` into a string for displaying with markdown.
    file_location = os.path.dirname(os.path.realpath(__file__))
    readme_path = os.path.abspath(os.path.join(file_location, '..', 'README.md'))

    with open(readme_path, 'r') as readme:
        content = readme.read()

    content_md = Markup(markdown.markdown(content))

    return render_template('about.html', **locals())


@app.route("/contact")
def contact():
    return render_template('home.html', title="Contact Me")


@app.route('/websearch', methods=['GET'])
def websearch():
    return render_template('websearch.html', title="Google Search")


@app.route('/v1/ws', methods=['POST'])
def ws_post():
    text = request.form['search terms']

    json_data = ws.search(text)

    return render_template('results.html',
                           search_type='web',
                           query=text,
                           length=len(json_data['items']),
                           results=json_data['items'],
                           title="Web Search Results")


@app.route("/elasticsearch")
def elasticsearch():
    tagline_ = es.get_status()

    if tagline_ != es.ES_SERVER_DOWN:
        return render_template('elasticsearch.html', status="AVAILABLE", title="Elasticsearch")
    else:
        return render_template('ESerror.html')


@app.route("/v1/es", methods=["GET"])
def es_get():
    # Parse search parameters
    args = request.args
    search_type = args['match']
    if search_type not in ['_all', '_id']:
        search_type = '_all'

    query = args['query']

    res = es.search(es.parse_query(search_type, query))
    if search_type == es.ES_SEARCH_ALL:
        return render_template('results.html',
                               search_type='elastic',
                               query=query,
                               length=len(res),
                               results=res,
                               title="ES Search Results")

    else: # search_type == es.ES_SEARCH_ID:
        return render_template('single_result.html',
                               artist=res[0]['Artist'],
                               song_title=res[0]['Song'],
                               year=res[0]['Year'],
                               rank=res[0]['Rank'],
                               lyrics=res[0]['Lyrics'],
                               title="Lyrics: {} - {}".format(res[0]['Song'], res[0]['Artist']))


if __name__ == '__main__':
    app.run()
