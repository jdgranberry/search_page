from flask import Flask, render_template, request
import configparser
import urllib.parse
import urllib.request
import json


app = Flask(__name__)

NUM_SEARCH_RESULTS = 10         # Valid values are integers between 1 and 10, inclusive.

# Pull in the API key to enable search
config = configparser.ConfigParser()
config.read('search_page.env')
api_key = config['Google Search API']['Apikey']
cx = config['Google Search API']['Cx']


@app.route('/')
def hello_world():
    return render_template('search.html', my_string="Hello World!", my_list=[0, 1, 2, 3, 4, 5])


@app.route("/home")
def home():
    return render_template('search.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5], title="Home")


@app.route("/about")
def about():
    return render_template('search.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5], title="About")


@app.route("/contact")
def contact():
    return render_template('search.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5], title="Contact Us")


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['search terms']

    params = {'key': api_key,
              'cx': cx,
              'q': text,
              'num': NUM_SEARCH_RESULTS}

    url = 'https://www.googleapis.com/customsearch/v1?%s' % urllib.parse.urlencode(params)
    # with urllib.request.urlopen(url) as f:
    #     json_data = json.loads(f.read().decode('utf-8'))

    # DEBUG CODE
    import os
    with open(os.path.abspath('/home/jdgranberry/Dropbox/College/CS4315 - Intro Data Mining/assignment_3/search_page/web/test_search.json'), 'r') as testdata:
        json_data = json.loads(testdata.read())

    return render_template('web_search_results.html',
                           query=text,
                           length=len(json_data['items']),
                           results=json_data['items'])

if __name__ == '__main__':
    app.run()
