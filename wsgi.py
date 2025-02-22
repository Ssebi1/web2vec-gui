import json

from flask import Flask, request, render_template
from lib.web2vec_controller import Web2VecController
from lib.serpapi_controller import SerpApiController

app = Flask(__name__)


@app.route('/ping')
def hello_world():
    return 'pong'


@app.route('/')
def home():
    predefined_url = request.args.get('url', '')
    return render_template('index.html', predefined_url=predefined_url)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    if request.method == 'POST':
        query = request.form['query']
        if not query:
            return 'Missing query', 400
        data = SerpApiController().search(query)
        return render_template('search_result.html', data=data, query=query)

@app.route('/search/test', methods=['GET'])
def search_test():
    data = json.load(open('static/data/example_search.json'))
    return render_template('search_result.html', data=data, query="sebastian dancau")


@app.route('/crawl', methods=['POST'])
def crawl():
    # Allow params:
    # - depth_limit (int)
    # - start_url (str)
    # - allowed_domains (list)
    # - extractors (list): [dns, html, http, certificate, url_geo, url_lexical, whois, google_index, open_page_rank, similar_web, url_haus]
    if request.method == 'POST':
        args = request.form
        if not args or 'url' not in args:
            return 'Missing url', 400
        data = Web2VecController().crawl(
            start_url=args['url'],
            depth_limit=int(args['depth']) if 'depth' in args else 1,
            allowed_domains=args.get('allowed_domains', None),
            extractors=args.getlist('extractors', None)
        )
        return render_template('crawl_result.html', data=data, url=args['url'])

@app.route('/crawl/test', methods = ['GET'])
def crawl_test():
    # load data from json file
    data = json.load(open('static/data/example_response.json'))
    return render_template('crawl_result.html', data=data, url="https://sebastian.dancau.net")


if __name__ == "__main__":
    app.run()