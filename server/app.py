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
    data =[{
        'id':one.id,
        'author':one.author,
        'title':one.title,
        'content':one.content,
        'preview':one.preview,
        'minutes_to_read':one.minutes_to_read
        }  for one in Article.query.all()]
    
    response=make_response(
        jsonify(data),
        200
    )
    return response

@app.route('/articles/<int:id>')
def show_article(id):
    
    session['page_views'] = 0 if not session.get('page_views') else session.get("page_views")
    session['page_views'] += 1
    
    if session['page_views'] <= 3 :
        
        data =Article.query.filter_by(id=id).first()
        
   
        response_dict=data.to_dict()

        response =make_response(
            jsonify(response_dict),
            200
        )
        
        return response
    
    return ({'message' :'Maximum pageview limit reached'},
    401)
    
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
