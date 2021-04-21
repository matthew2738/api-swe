import json
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    image = db.Column(db.String(100))
    zip = db.Column(db.Integer)
    city = db.Column(db.String(50))
    category = db.Column(db.String(50))
    postdate = db.Column(db.Integer)
    startdate = db.Column(db.Integer)
    enddate = db.Column(db.Integer)
    description = db.Column(db.Text)

    def __repr__ (self):
        return f"{self.title} - {self.description}"

@app.route("/")
def home():
    return "Hello, This is the API for the SWE Class"

@app.route('/posts')
def get_posts():
    posts = Post.query.all()
    
    output = []
    for post in posts:
        post_data = {
            'id' : post.id,
            'title': post.title,
            'image' : post.image,
            'zip' : post.zip,
            'city' : post.city,
            'category' : post.category,
            'postdate' : post.postdate,
            'startdate' : post.startdate,
            'enddate' : post.enddate,
            'description': post.description
            }
        output.append(post_data)
    return {"posts" : output}

@app.route("/posts/<id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    return {"title": post.title, "description": post.description}

@app.route('/posts', methods=['POST'])
def add_post():
    post = Post(title=request.json['title'],
                image=request.json['image'],
                zip=request.json['zip'],
                city=request.json['city'],
                category=request.json['category'],
                postdate=request.json['postdate'],
                startdate=request.json['startdate'],
                enddate=request.json['enddate'],
                description=request.json['description'])
    db.session.add(post)
    db.session.commit()
    return {'id': post.id}

@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"error": "not found"}
    db.session.delete(post)
    db.session.commit()
    return {"message": "Deleted"}
