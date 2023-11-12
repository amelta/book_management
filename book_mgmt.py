from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Funktionale Programmierung: Immutable Values
def add_book(new_book):
    db.session.add(new_book)
    db.session.commit()

# Funktionale Programmierung: Map, Filter und Reduce
def get_book_titles():
    return [book.title for book in Book.query.all()]

def filter_books_by_year(year):
    return Book.query.filter_by(year=year).all()

def count_books():
    return Book.query.count()

# Beispiel-Routen
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_new_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = int(request.form.get('year'))

        new_book = Book(title=title, author=author, year=year)
        add_book(new_book)

        # Redirect to a confirmation page with book details
        return redirect(url_for('book_confirmation', title=title, author=author, year=year))

    # If it's a GET request, render a form to add a new book
    return render_template('add_book_form.html')

@app.route('/add_new_book_form')
def add_new_book_form():
    return render_template('add_book_form.html')

@app.route('/book_confirmation/<title>/<author>/<int:year>')
def book_confirmation(title, author, year):
    # Render a confirmation template with book details
    return render_template('book_confirmation.html', title=title, author=author, year=year)

@app.route('/book_list_with_button')
def book_list_with_button():
    # Display the book list with a button
    return render_template('book_list_with_button.html', books=Book.query.all())

@app.route('/books_in_year/<int:year>')
def books_in_year(year):
    filtered_books = filter_books_by_year(year)
    return render_template('books_in_year.html', year=year, books=filtered_books)

@app.route('/total_books')
def total_books():
    return f'Total number of books: {count_books()}'

if __name__ == '__main__':
    app.run(debug=True)
