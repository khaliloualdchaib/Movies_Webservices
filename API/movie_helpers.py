import requests
from config import API_KEY
def getGenre(genreID):
    """
    get the genre information based on the given id.
    """
    response = requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}")
    data = response.json()
    for genre in data["genres"]:
        if genreID == genre["id"]:
            return genre["name"]

def getActors(movieID, mustHave_actors = None):
    """
    get the first two actors of the given movie.
    """
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movieID}/credits?api_key={API_KEY}')
    # parse response and extract actors
    data = response.json()
    cast = data.get('cast', [])
    if mustHave_actors is None:
        actors = [c['name'] for c in cast[:2]] 
        return actors
    return mustHave_actors