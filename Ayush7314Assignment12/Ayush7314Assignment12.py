# Ayush7314Assignment12.py
from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__, template_folder='.')  # Set template folder to current directory

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['library_management']
books_collection = db['books']

@app.route('/')
def index():
    books = books_collection.find()
    return render_template('Ayush7314Assignment12.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'isbn': request.form['isbn'],
            'status': request.form['status'],
            'copies_available': int(request.form['copies'])
        }
        books_collection.insert_one(book)
        flash('Book added successfully!')
        return redirect('/')
    return render_template('Ayush7314Assignment12.html', show_add_form=True)

@app.route('/edit/<id>', methods=['POST'])
def edit_book(id):
    updated_book = {
        'title': request.form['title'],
        'author': request.form['author'],
        'isbn': request.form['isbn'],
        'status': request.form['status'],
        'copies_available': int(request.form['copies'])
    }
    books_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_book})
    return redirect('/')

@app.route('/delete/<id>')
def delete_book(id):
    books_collection.delete_one({'_id': ObjectId(id)})
    return redirect('/')

@app.route('/search', methods=['POST'])
def search_books():
    search_term = request.form['search']
    query = {
        '$or': [
            {'title': {'$regex': search_term, '$options': 'i'}},
            {'author': {'$regex': search_term, '$options': 'i'}},
            {'isbn': {'$regex': search_term, '$options': 'i'}}
        ]
    }
    books = books_collection.find(query)
    return render_template('Ayush7314Assignment12.html', books=books, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)