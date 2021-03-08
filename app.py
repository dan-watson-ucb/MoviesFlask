from flask import Flask, render_template, request
from movie_functions import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    print(app.root_path)
    return render_template('index.html')


@app.route('/results/', methods=['POST'])
def process():
    index_page = False
    movie_title = request.form['movie_name']
    movies = find_movies(movie_title)
    if movies['results'] is None:
        success = False
        search_again = True
    else:
        success = True
        search_again = False
    return render_template("index.html", **locals())


@app.route('/review/', methods=['GET', 'POST'])
def return_review():
    movie_url = request.form.getlist('name')[0]
    review_data = pull_review(movie_url)
    review_text = get_review_text(review_data)
    sentiment, positive, neutral, negative, mixed = get_score(review_text)
    return render_template('review.html', **locals())


if __name__ == '__main__':
    app.run()
