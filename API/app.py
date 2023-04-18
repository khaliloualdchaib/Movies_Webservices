from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


from resources.movie import Movie
from resources.popular import Popular
from resources.similar_genre import SimilarGenre
from resources.similar_runtime import SimilarRuntime
from resources.overlapping_actors import OverlappingActors
from resources.liked import Liked
from resources.barplot import BarPlot

SWAGGER_URL = '/api/manual'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)
def app():
    app = Flask(__name__)
    app.register_blueprint(swaggerui_blueprint)
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