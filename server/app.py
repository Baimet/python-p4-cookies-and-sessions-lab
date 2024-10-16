#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])

@app.route('/articles/<int:id>')
def show_article(id):
    # Set the initial value of session['page_views'] if it doesn't exist
    session['page_views'] = session.get('page_views', 0)
    
    # Increment the page view count
    session['page_views'] += 1

    # Check if page views are within the allowed limit
    if session['page_views'] > 3:
        # If the user has viewed more than 3 articles, return an error message
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # If within the limit, return the article
    article = Article.query.get(id)
    if article:
        return jsonify(article.to_dict())
    else:
        return jsonify({'message': 'Article not found'}), 404



if __name__ == '__main__':
    app.run(port=5555)
