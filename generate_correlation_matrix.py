# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 09:59:41 2020

@author: Welcome
"""

import pandas as pd
from scipy import sparse
import pickle

ratings = pd.read_csv('ml1m_ratings.csv', 
                      sep='\t', 
                      usecols=['userid', 'movieid', 'user_emb_id', 'movie_emb_id', 'rating'])

movies = pd.read_csv('ml1m_movies.csv', 
              sep='\t',
              usecols=['movieid', 'title', 'genre'])

#movies.to_csv("movies.csv")


ratings = pd.merge(movies,ratings).drop(['genre','user_emb_id','movie_emb_id'],axis=1)

userRatings = ratings.pivot_table(index=['userid'],columns=['title'],values=['rating'])

userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)

corrMatrix = userRatings.corr(method='pearson')
corrMatrix.head(10)

with open('corrmatrix.pickle', 'wb') as f:
    pickle.dump(corrMatrix, f)
    
