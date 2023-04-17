from flask_restful import Resource, reqparse
import requests
from config import *
import re

class BarPlot(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('movies', type=str)
        arguments = parser.parse_args()
        ids = arguments['movies']
        pattern = r"^\d+(,\s*\d+)*$"
        if ids is None:
            return APIresponse([], 400, "No id's were given.")
        if len(ids) == 0:
            return APIresponse([], 400, "No id's were given.")
        if not re.match(pattern, ids):
            return APIresponse([], 400, "Please enter valid query of the right form")
        id_list = ids.split(',')
        avgs = []
        movienames = []
        for movie in id_list:
            response = requests.get(f'{self.base_url}/movie/{movie}?api_key={API_KEY}')
            if response.status_code == 200:
                if movie in DELETED:
                    return APIresponse([], 404, f"Movie with id {movie} does not exist.")
                data = response.json()
                movienames.append(data["original_title"])
                avgs.append(data["vote_average"])
            else:
                return APIresponse([], 404, f"Movie with id {movie} does not exist.")
        quickchart_url = 'https://quickchart.io/chart/create'
        post_data = {'chart': {'type': 'bar', 'data': {'labels': movienames,
             'datasets': [{'label': 'Vote Average', 'data': avgs}]}}}
        response = requests.post(
            quickchart_url,
            json=post_data,
        )
        if response.json()["success"]:
            return APIresponse(response.json()["url"], 200, "OK")
        return APIresponse("", 400, "Bad Request") 