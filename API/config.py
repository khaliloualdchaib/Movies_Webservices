from flask import make_response
import json
API_KEY = ''
def dataItem(title, id, genres, actors):
    return {
        'title': title,
        'id': id,
        'actors': actors,
        'genres': genres,
    }

def APIresponse(data, status, message):
    response_data =  {
        'data': data, 
        'message': message
    }
    response = make_response(json.dumps(response_data))
    response.status_code = status
    response.headers['Content-Type'] = 'application/json'
    return response
DELETED = set()
LIKED = set()
