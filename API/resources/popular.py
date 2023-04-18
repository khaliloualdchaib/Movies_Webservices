from flask_restful import Resource
from flask import request
import requests
from config import *
from movie_helpers import *

class Popular(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    def get(self):
        """
        Gets the first x popular movies
        """ 
        try:
            movies = []
            amount = request.args.get('limit')
            if amount is None:
                amount = 20
            else:
                amount = int(amount)
            #calculate number of pages
            pages = (amount-1) // 20 + 1
            for page in range(1, pages+1):
                response = requests.get(f'{self.base_url}/movie/popular?api_key={API_KEY}&page={page}')
                data = response.json()
                totalItems = len(data["results"])
                for index in range(totalItems):
                    if data["results"][index]['id'] in DELETED:
                        if index == 19:
                            amount = amount + 1
                            pages = (amount-1) // 20 + 1
                        else:
                            totalItems += 1
                    else:
                        id = data["results"][index]['id']
                        genres = [getGenre(genre) for genre in data["results"][index]['genre_ids']]
                        movies.append(dataItem(title=data["results"][index]['title'], id=id, actors=getActors(id), genres=genres))
            #only take the first n=amount movies
            movies = movies[:amount]
            return APIresponse(movies, 200, "OK")
        except:
            return APIresponse([], 400, "The 'limit' query parameter is missing or invalid")