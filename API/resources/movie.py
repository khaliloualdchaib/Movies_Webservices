from flask_restful import Resource, reqparse
import requests
from config import *
from movie_helpers import *

class Movie(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"

    def get(self, movie_id=None):
        if movie_id is None:
            """
            Given a movie(title) return the corresponding movies.
            """
            parser = reqparse.RequestParser()
            parser.add_argument('movie_title', type=str)
            arguments = parser.parse_args()
            title = arguments['movie_title']
            response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}&append_to_response=runtime')
            data = response.json()
            if len(data['results']) == 0:
                return APIresponse([], 404, "Movie not Found.")
            if title is None:
                return APIresponse([], 204, "No Content")
            movies = []
            for i in range(len(data['results'])):
                if data['results'][i]['id'] not in DELETED:
                    genres = [getGenre(g) for g in data['results'][i]['genre_ids']]
                    date =  data['results'][i]['release_date'] if 'release_date' in data['results'][i] else "Unknown"
                    id = data['results'][i]['id']
                    runtime = requests.get(f'{self.base_url}/movie/{id}?api_key={API_KEY}').json()['runtime']
                    movies.append(dataItem(title=data['results'][i]['title'], id=id, actors=getActors(id), genres=genres, runtime=runtime, release_date=date))
            return APIresponse(movies,200, "OK")
        else:
            """
            Given a movie(id) return the corresponding movie.
            """
            if movie_id not in DELETED:
                response = requests.get(f'{self.base_url}/movie/{movie_id}?api_key={API_KEY}')
                if response.status_code == 200:
                    genres = [getGenre(g['id']) for g in  response.json()['genres']]
                    date = response.json()['release_date'] if 'release_date' in response.json() else "Unknown"
                    data = [dataItem(title=response.json()['title'], id=response.json()['id'], actors=getActors(response.json()['id']), genres=genres, runtime=response.json()['runtime'], release_date=date)]
                    return APIresponse(data, 200, "OK")
            return APIresponse([], 404, "Movie not Found.")
    def delete(self, movie_id=None):
        if movie_id is None:
            return APIresponse([], 400, "No movie was given.")
        DELETED.add(movie_id)
        return APIresponse([], 200, "Movie deleted succesfully.")