from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
from flask_table import Table, Col

#building flask table for showing recommendation results
class Results(Table):
    id = Col('Id', show=False)
    title = Col('Recommendation List')

app = Flask(__name__)

#Welcome Page
@app.route("/")
def welcome():
    return render_template('welcome.html')

#Rating Page
@app.route("/rating", methods=["GET", "POST"])
def rating():
    if request.method=="POST":
        return render_template('recommendation.html')
    return render_template('rating.html')

#Results Page
@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    if request.method == 'POST':
        #reading the original dataset
        #movies = pd.read_csv('movies.csv')

        #separating genres for each movie
        #movies = pd.concat([movies, movies.genres.str.get_dummies(sep='|')], axis=1)

        #dropping variables to have a dummy 1-0 matrix of movies and their genres
        ## IMAX is not a genre, it is a specific method of filming a movie, thus removed
        ###we do not need movieId for this project
        #categories = movies.drop(['title', 'genres', 'IMAX', 'movieId'], axis=1)

        #initializing user preference list which will contain user ratings
        
        with open('corrmatrix.pickle', 'rb') as f:
            corrmatrix = pickle.load(f)
        
        corrMatrix = corrmatrix['rating'].droplevel(level=0)
    
        
        
        movies_list = [
            'Bad Boys (1995)',
            'Firewalker (1986)',
            'Toy Story (1995)',
            'Alice in Wonderland (1951)',
            'My Chauffeur (1986)',
            'Gang Related (1997)',
            "Jupiter's Wife (1994)",
            'Godfather, The (1972)',
            'American Pimp (1999)',
            "Killer's Kiss (1955)",
            'Baraka (1992)',
            'King and I, The (1956)',
            "Mike's Murder (1984)",
            'Love Is a Many-Splendored Thing (1955)',
            "Star Wars: Episode I - The Phantom Menace (1999)",
            'Braveheart (1995)',
            'Seven (Se7en) (1995)',
            'Good, The Bad and The Ugly, The (1966)']
        
        preferences = []

        #reading rating values given by user in the front-end
        Action = request.form.get('Action')
        Adventure = request.form.get('Adventure')
        Animation = request.form.get('Animation')
        Children = request.form.get('Children')
        Comedy = request.form.get('Comedy')
        Crime = request.form.get('Crime')
        Documentary = request.form.get('Documentary')
        Drama = request.form.get('Drama')
        Fantasy = request.form.get('Fantasy')
        FilmNoir = request.form.get('FilmNoir')
        Horror = request.form.get('Horror')
        Musical = request.form.get('Musical')
        Mystery = request.form.get('Mystery')
        Romance = request.form.get('Romance')
        SciFi = request.form.get('SciFi')
        Thriller = request.form.get('Thriller')
        War = request.form.get('War')
        Western = request.form.get('Western')

        #inserting each rating in a specific position based on the movie-genre matrix
        preferences.append(int(Action))
        preferences.append(int(Adventure))
        preferences.append(int(Animation))
        preferences.append(int(Children))
        preferences.append(int(Comedy))
        preferences.append(int(Crime))
        preferences.append(int(Documentary))
        preferences.append(int(Drama))
        preferences.append(int(Fantasy))
        preferences.append(int(FilmNoir))
        preferences.append(int(Horror))
        preferences.append(int(Musical))
        preferences.append(int(Mystery))
        preferences.append(int(Romance))
        preferences.append(int(SciFi))
        preferences.append(int(War))
        preferences.append(int(Thriller))
        preferences.append(int(Western))

        #This funtion will get each movie score based on user's ratings through dot product
        tuple_movie_n_rating = list(zip(movies_list,preferences))

        #Generating recommendations based on top score movies
        def get_similar(movie_name,rating):
            similar_ratings = corrMatrix[movie_name]*(rating-2.5)
            similar_ratings = similar_ratings.sort_values(ascending=False)
            #print(type(similar_ratings))
            return similar_ratings
        
        def recommendations(list_of_tuple):
            similar_movies = pd.DataFrame()
            for movie,rating in list_of_tuple:
                similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)
            
            mann = similar_movies.sum().sort_values(ascending=False).index.values
            return [m for m in mann if not m in movies_list][:20] 

        #def recommendations(X, n_recommendations):
            #movies['score'] = get_score(categories, preferences)
            #return movies.sort_values(by=['score'], ascending=False)['title'][:n_recommendations]

        #printing top-20 recommendations
        output= recommendations(tuple_movie_n_rating)
        table = Results(output)
        table.border = True
        return render_template('recommendation.html', table=table)

if __name__ == '__main__':
   app.run(debug = True)