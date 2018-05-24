from flask_script import Manager
from movie import app, db, Director, Movie

manager = Manager(app)


# reset the database and create some initial data
@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    StevenSpielberg = Director(name='Steven Spielberg', about='Steven Spielberg is an American filmmaker and the highest grossing filmmaker of all time')
    RyanCoogler = Director(name='Ryan Coogler', about='Ryan Coogler is an up and coming director known for his movies Creed and Black Panther')
    JJAbrams = Director(name='JJ Abrams', about='JJ Abrams is a director well known for his Star Trek and Star Wars movies')
    movie1 = Movie(name='Jurassic Park', year=1993, ratings="IMDb: 8.1, Rotten Tomatoes: 92%", director=StevenSpielberg)
    movie2 = Movie(name='BlackPanther', year=2018, ratings="IMDb: 7.6, Rotten Tomatoes: 97%", director=RyanCoogler)
    movie3 = Movie(name='Star Wars: The Force Awakens', year=2015, ratings="IMDb: 8, Rotten Tomatoes: 93%", director=JJAbrams)
    db.session.add(StevenSpielberg)
    db.session.add(RyanCoogler)
    db.session.add(JJAbrams)
    db.session.add(movie1)
    db.session.add(movie2)
    db.session.add(movie3)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
