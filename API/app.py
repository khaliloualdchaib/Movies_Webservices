from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.movie import Movie
from resources.popular import Popular
from resources.similar_genre import SimilarGenre
from resources.similar_runtime import SimilarRuntime
from resources.overlapping_actors import OverlappingActors
from resources.liked import Liked
from resources.barplot import BarPlot

def app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)
    api.add_resource(Movie, '/api/movies', '/api/movies/<int:movie_id>')
    api.add_resource(Popular, '/api/movies/popular')
    api.add_resource(SimilarGenre, '/api/movies/<int:movie_id>/similar-genres')
    api.add_resource(SimilarRuntime, '/api/movies/<int:movie_id>/similar-runtime')
    api.add_resource(OverlappingActors, '/api/movies/<int:movie_id>/overlapping-actors')
    api.add_resource(Liked, '/api/liked-movies', '/api/liked-movies/<int:movie_id>')
    api.add_resource(BarPlot, '/api/movies/barplot')
    return app

app = app()
if __name__ == "__main__":
    app.run(debug=True)