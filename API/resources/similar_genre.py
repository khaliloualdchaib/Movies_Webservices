from flask_restful import Resource
import requests
from config import *
from movie_helpers import *
class SimilarGenre(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    def get(self, movie_id=None):
        """
        Given a movie id, return the movies that have exactly the same genres
        """
        if movie_id is None:
            return APIresponse([], 400, "Movie id needed!")
        response = requests.get(f'{self.base_url}/movie/{movie_id}?api_key={API_KEY}')
        if response.status_code == 404:
            return APIresponse([], 404, "Movie not found.")
        data = response.json()
        genres = data['genres']
        genre_ids = "" #for the request needed
        for genre in genres:
            genre_ids += str(genre['id']) + ','
        genre_ids = genre_ids[:-1] #remove the last ,
        response = requests.get(f'{self.base_url}/discover/movie/?api_key={API_KEY}&with_genres={genre_ids}')
        data = response.json()
        movies = []
        for movie in data["results"]:
            if movie['id'] not in DELETED:
                #add the movie only if the given movie genres are a subset of the current movie
                genres = [getGenre(genre) for genre in movie['genre_ids']]
                date = movie['release_date'] if 'release_date' in movie else "Unknown"
                id = movie["id"]
                runtime = requests.get(f'{self.base_url}/movie/{id}?api_key={API_KEY}').json()['runtime']
                movies.append(dataItem(title= movie['title'], id=id, actors=getActors(id), genres=genres, runtime=runtime, release_date=date))
        return APIresponse(movies, 200, "OK")