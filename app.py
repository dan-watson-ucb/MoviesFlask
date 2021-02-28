from flask import Flask, render_template, request
from movie_functions import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    index_page = True
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

@app.route('/results/review/', methods = ['POST'])
def return_review(movie_title, movies):

    film = movies['results'][movie]
    film_url = film['link']['url']
    review_raw = pull_review(film_url)

    review_text = get_review_text(review_raw)
    return render_template('review.html', **locals())


if __name__ == '__main__':
    app.run()
