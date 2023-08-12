from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from model import db, Movie
from form import UpdateForm, AddMovie
import requests
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
URL = "https://api.themoviedb.org/3/search/movie"
API_KEY = os.environ.get('api_key')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(app)


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route('/update/<int:fid>', methods=['POST', 'GET'])
def update(fid):
    form = UpdateForm()
    if form.validate_on_submit():
        update_ = db.get_or_404(Movie, fid)
        update_.rating = form.rating.data
        update_.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddMovie()
    if form.validate_on_submit():
        response = requests.get(url=URL, params={"api_key": API_KEY, "query": form.title.data})
        data = response.json()["results"]
        return render_template('select.html', movies=data)

    return render_template('add.html', form=form)


@app.route('/delete')
def delete():
    del_id = request.args.get('id')
    movie = db.get_or_404(Movie, del_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/selected')
def selected():
    movie_id = request.args.get('select')
    response = requests.get(url=f'https://api.themoviedb.org/3/movie/{movie_id}', params={'api_key': API_KEY})
    data = response.json()
    str_year = data['release_date']
    year = str_year[:4]
    new_movie = Movie(title=data['title'], img_url=f'https://image.tmdb.org/t/p/original{data["poster_path"]}',
                      year=int(year), description=data['overview'])
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('update', fid=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
