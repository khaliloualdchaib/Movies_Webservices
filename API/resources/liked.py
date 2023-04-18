from flask_restful import Resource
import requests
from config import *
from movie_helpers import *

class Liked(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    def get(self):
        movies = []
        for i in LIKED:
            response = requests.get(f'{self.base_url}/movie/{i}?api_key={API_KEY}')
            genres = [getGenre(g['id']) for g in  response.json()['genres']]
            data = dataItem(title=response.json()['title'], id=response.json()['id'], actors=getActors(response.json()['id']), genres=genres)
            movies.append(data)
        return APIresponse(movies, 200, "OK")

    def post(self, movie_id):
        if movie_id in LIKED:
            return APIresponse([], 400, "Movie Already Liked.")
        response = requests.get(f'{self.base_url}/movie/{movie_id}?api_key={API_KEY}')
        if response.status_code == 404 or movie_id in DELETED:
            return APIresponse([], 404, "Movie not found.")
        LIKED.add(movie_id)
        return APIresponse([], 200, "OK")
    
    def delete(self, movie_id):
        response = requests.get(f'{self.base_url}/movie/{movie_id}?api_key={API_KEY}')
        if response.status_code == 404:
            return APIresponse([], 404, "Movie not found.")
        if movie_id in LIKED:
            LIKED.remove(movie_id)
            return APIresponse([], 200, "OK")
        return APIresponse([], 400, "Movie Not Liked.")