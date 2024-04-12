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

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    response = make_response(
        jsonify(articles),
        200
    )
    return response
    pass

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1
    
    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()
        article_data = article.to_dict()
        return jsonify(article_data), 200
    else:
        error_message = {'message': 'Maximum pageview limit reached'}
        return jsonify(error_message), 401

    pass

if __name__ == '__main__':
    app.run(port=5555)
