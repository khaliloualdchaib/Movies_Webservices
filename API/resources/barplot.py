from flask_restful import Resource
from flask import request
import requests
from config import *
import re

class BarPlot(Resource):
    def __init__(self) -> None:
        self.base_url = "https://api.themoviedb.org/3"
    def get(self):
        ids = request.args.get('movies')
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
            print(DELETED, str(movie))
            if response.status_code == 404 or int(movie) in DELETED:
                return APIresponse([], 404, f"Movie with id {movie} does not exist.")
            elif response.status_code == 200:
                data = response.json()
                movienames.append(data["original_title"])
                avgs.append(data["vote_average"])
            else:
                return APIresponse([], 400, "Bad request")
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