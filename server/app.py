#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
app.secret_key = 'your-secret-key'

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(articles, 200)

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    article = Article.query.filter_by(id=id).first()

    # Check if 'page_views' exists in the session, and set it to 0 if it doesn't
    session['page_views'] = session.get('page_views', 0)

    # Increment the page view count for the user
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:

        return make_response(article.to_dict(), 200)

    # User has viewed more than 3 pages, return an error message
    error_message = {'message': 'Maximum pageview limit reached'}
    return make_response(error_message, 401)

if __name__ == '__main__':
    app.run(port=5555)
