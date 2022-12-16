import requests
import json
from .config import food_search_key, recipe_search_key

def food_search(input):
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"
    querystring = {"query": {input}}
    headers = food_search_key
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

def recipe_search(input):
    url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"
    querystring = {"query": {input}}
    headers = recipe_search_key
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)
