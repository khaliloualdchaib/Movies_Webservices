from flask_restful import Resource
import requests
from config import *
from movie_helpers import *

class SimilarRuntime(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    def get(self, movie_id=None):
        """
        Given a movie, return the movies that have a similar runtime. (You can
        assume a similar runtime has a maximum of 10 minutes difference)
        """
        response = requests.get(f'{self.base_url}/movie/{movie_id}?api_key={API_KEY}')
        data = response.json()
        if movie_id is None:
            return APIresponse([], 400, "Movie id needed!")
        if response.status_code == 404:
             return APIresponse([], 404, "Movie not Found.")
        runtime = data['runtime']
        min_runtime = max(0, runtime - 10)
        max_runtime = runtime + 10
        response = requests.get(f'{self.base_url}/discover/movie?api_key={API_KEY}&with_runtime.gte={min_runtime}&with_runtime.lte={max_runtime}&language=en-US')
        data = response.json()
        movies = []

        for movie in data["results"]:
            if movie['id'] not in DELETED:
                genres = [getGenre(g) for g in movie['genre_ids']]
                date = movie['release_date'] if 'release_date' in movie else "Unknown"
                id = movie["id"]
                runtime = requests.get(f'{self.base_url}/movie/{id}?api_key={API_KEY}').json()['runtime']
                movies.append(dataItem(title=movie['title'], id=id, actors=getActors(id), genres=genres, runtime=runtime, release_date=date))
        return APIresponse(movies, 200, "OK")