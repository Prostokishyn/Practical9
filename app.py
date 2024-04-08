import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

    def serialize(self):
        current_category = Category.query.get(self.category_id)
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "category": current_category.name
        }

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.publication_year}', '{self.category_id}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"Category('{self.name}')"

class UserResource(Resource):
    def get(self, user_id):
        current_user = User.query.get(user_id)
        return current_user.serialize()
api.add_resource(UserResource, '/users/<int:user_id>')    

class BooksResource(Resource):
    def get(self, book_id):
        current_book = Book.query.get(book_id)
        return current_book.serialize()
api.add_resource(BooksResource, '/books/<int:book_id>')           

class CategoryResource(Resource):
    def get(self, category_id):
        current_category = Category.query.get(category_id)
        return current_category.serialize()
api.add_resource(CategoryResource, '/categories/<int:category_id>')   

if __name__ == "__main__":
    app.run(debug=True)