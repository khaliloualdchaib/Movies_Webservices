from flask_restful import Resource, reqparse
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
            parser = reqparse.RequestParser()
            parser.add_argument('limit', type=int, default=20)
            arguments = parser.parse_args()
            amount = arguments['limit']
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
                        runtime = requests.get(f'{self.base_url}/movie/{id}?api_key={API_KEY}').json()['runtime']
                        genres = [getGenre(genre) for genre in data["results"][index]['genre_ids']]
                        date =  data["results"][index]['release_date'] if 'release_date' in data["results"][index] else "Unknown"
                        movies.append(dataItem(title=data["results"][index]['title'], id=id, actors=getActors(id), genres=genres, runtime=runtime, release_date=date))
            #only take the first n=amount movies
            movies = movies[:amount]
            print(movies)
            return APIresponse(movies, 200, "OK")
        except:
            return APIresponse([], 400, "The 'limit' query parameter is missing or invalid")