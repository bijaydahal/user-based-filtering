# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 11:14:49 2020

@author: Welcome
"""

import pandas as pd
import pickle


with open('corrmatrix.pickle', 'rb') as f:
    corrmatrix = pickle.load(f)
    
corrMatrix = corrmatrix['rating'].droplevel(level=0)

def get_similar(movie_name,rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    #print(type(similar_ratings))
    return similar_ratings

romantic_lover = [("Toy Story (1995)",5),("GoldenEye (1995)",3),("Casino (1995)",1),("Four Rooms (1995)",2)]
similar_movies = pd.DataFrame()
for movie,rating in romantic_lover:
    similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)

mann = similar_movies.sum().sort_values(ascending=False).head(20).index.values
mann = similar_movies.sum().sort_values(ascending=False).index.values
print([m for m in mann if not m in movies_list][:20]) 