import os
from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# define database tables
class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    movies = db.relationship('Movie', backref='director', cascade="delete")


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    year = db.Column(db.Integer)
    ratings = db.Column(db.Text)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page<h1>"
    return render_template('index.html')


@app.route('/directors')
def show_all_directors():
    directors = Director.query.all()
    return render_template('director-all.html', directors=directors)


@app.route('/director/add', methods=['GET', 'POST'])
def add_directors():
    if request.method == 'GET':
        return render_template('director-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        about = request.form['about']

        # insert the data into the database
        director = Director(name=name, about=about)
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('show_all_directors'))


@app.route('/api/director/add', methods=['POST'])
def add_ajax_directors():
    # get data from the form
    name = request.form['name']
    about = request.form['about']

    # insert the data into the database
    director = Director(name=name, about=about)
    db.session.add(director)
    db.session.commit()
    # flash message type: success, info, warning, and danger from bootstrap
    flash('Director Inserted', 'success')
    return jsonify({"id": str(director.id), "name": director.name})


@app.route('/director/edit/<int:id>', methods=['GET', 'POST'])
def edit_director(id):
    director = Director.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('director-edit.html', director=director)
    if request.method == 'POST':
        # update data based on the form data
        director.name = request.form['name']
        director.about = request.form['about']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_directors'))


@app.route('/director/delete/<int:id>', methods=['GET', 'POST'])
def delete_director(id):
    director = Director.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('director-delete.html', director=director)
    if request.method == 'POST':
    
        db.session.delete(director)
        db.session.commit()
        return redirect(url_for('show_all_directors'))


@app.route('/api/director/<int:id>', methods=['DELETE'])
def delete_ajax_director(id):
    director = Director.query.get_or_404(id)
    db.session.delete(director)
    db.session.commit()
    return jsonify({"id": str(director.id), "name": director.name})


@app.route('/movies')
def show_all_movies():
    movies = Movie.query.all()
    return render_template('movie-all.html', movies=movies)


@app.route('/movie/add', methods=['GET', 'POST'])
def add_movies():
    if request.method == 'GET':
        directors = Director.query.all()
        return render_template('movie-add.html', directors=directors)
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        year = request.form['year']
        ratings = request.form['ratings']
        director_name = request.form['director']
        director = Director.query.filter_by(name=director_name).first()
        movie = Movie(name=name, year=year, ratings=ratings, director=director)

        # insert the data into the database
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('show_all_movies'))


@app.route('/movie/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.filter_by(id=id).first()
    directors = Director.query.all()
    if request.method == 'GET':
        return render_template('movie-edit.html', movie=movie, directors=directors)
    if request.method == 'POST':
        # update data based on the form data
        movie.name = request.form['name']
        movie.year = request.form['year']
        movie.ratings = request.form['ratings']
        director_name = request.form['director']
        director = Director.query.filter_by(name=director_name).first()
        movie.director = director
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_movies'))


@app.route('/movie/delete/<int:id>', methods=['GET', 'POST'])
def delete_movie(id):
    movie = Movie.query.filter_by(id=id).first()
    directors = Director.query.all()
    if request.method == 'GET':
        return render_template('movie-delete.html', movie=movie, directors=directors)
    if request.method == 'POST':


        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('show_all_movies'))


@app.route('/api/movie/<int:id>', methods=['DELETE'])
def delete_ajax_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"id": str(movie.id), "name": movie.name})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def show_all_users():
    return render_template('user-all.html')


@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    # how to get form data is different for GET vs. POST
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        # return render_template('form-demo.html', first_name=first_name)
        return redirect(url_for('form_demo'))


@app.route('/user/<string:name>/')
def get_user_name(name):
    # return "hello " + name
    # return "Hello %s, this is %s" % (name, 'administrator')
    return render_template('user.html', name=name)


@app.route('/movie/<int:id>/')
def get_movie_id(id):

    return "Hi, this is %s and the movie's id is %d" % ('administrator', id)


if __name__ == '__main__':


    app.run()
