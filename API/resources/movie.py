from flask_restful import Resource
from flask import request
import requests
from config import *
from movie_helpers import *

class Movie(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"

    def get(self, movie_id=None):
        print(DELETED)
        if movie_id is None:
            """
            Given a movie(title) return the corresponding movies.
            """
            title = request.args.get('movie_title')
            response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}&append_to_response=runtime')
            if response.status_code == 200:
                data = response.json()
                if len(data['results']) == 0:
                    return APIresponse([], 404, "Movie not Found.")
                if title is None:
                    return APIresponse([], 204, "No Content")
                movies = []
                for i in range(len(data['results'])):
                    if data['results'][i]['id'] not in DELETED:
                        genres = [getGenre(g) for g in data['results'][i]['genre_ids']]
                        id = data['results'][i]['id']
                        movies.append(dataItem(title=data['results'][i]['title'], id=id, actors=getActors(id), genres=genres))
                return APIresponse(movies,200, "OK")
            elif response.status_code == 404:
                return APIresponse(movies,404, "Movie not Found.")
            else:
                return APIresponse(movies,400, "Bad Request")
        else:
            """
            Given a movie(id) return the corresponding movie.
            """
            if movie_id not in DELETED:
                response = requests.get(f'{self.base_url}/movie/{movie_id}?api_key={API_KEY}')
                if response.status_code == 200:
                    genres = [getGenre(g['id']) for g in  response.json()['genres']]
                    data = [dataItem(title=response.json()['title'], id=response.json()['id'], actors=getActors(response.json()['id']), genres=genres)]
                    return APIresponse(data, 200, "OK")
                elif response.status_code == 404:
                    return APIresponse([], 404, "Movie not Found.")
                else:
                    return APIresponse([], 400, "Bad Request")
            return APIresponse([], 404, "Movie not Found.")
    def delete(self, movie_id=None):
        if movie_id is None:
            return APIresponse([], 400, "No movie was given.")
        if movie_id in DELETED:
            return APIresponse([], 404, "Movie not Found.")
        if movie_id in LIKED:
            LIKED.remove(movie_id)
        DELETED.add(movie_id)
        return APIresponse([], 200, "Movie deleted succesfully.")