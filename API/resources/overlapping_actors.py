from flask_restful import Resource, reqparse
import requests
from config import *
from movie_helpers import *

class OverlappingActors(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    
    def get(self, movie_id):
        response = requests.get(f'{self.base_url}/movie/{movie_id}/credits?api_key={API_KEY}')
        data = response.json()
        if response.status_code == 404 or movie_id in DELETED:
            return APIresponse([], 404, "Movie not Found.")
        cast = data["cast"]
        actor1_id = cast[0]['id']
        actor2_id = cast[1]['id']
        movies = []
        response =  requests.get(f'{self.base_url}/discover/movie?api_key={API_KEY}&with_cast={actor1_id},{actor2_id}')
        data = response.json()
        for movie in data["results"]:
            if movie['id'] not in DELETED:
                genres = [getGenre(g) for g in movie['genre_ids']]
                date =  movie['release_date'] if 'release_date' in movie else "Unknown"
                id = movie["id"]
                runtime = requests.get(f'{self.base_url}/movie/{id}?api_key={API_KEY}').json()['runtime']
                movies.append(dataItem(title=movie['title'], id= id, actors=getActors(id, [cast[0]['name'], cast[1]['name']]), genres=genres, runtime=runtime, release_date=date))
        return APIresponse(movies, 200, "OK")