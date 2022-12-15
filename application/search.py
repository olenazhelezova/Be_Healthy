import requests
import json

def food_search(input):
    url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"
    querystring = {"query": {input}}
    headers = {
        "X-RapidAPI-Key": "9a22f3cf69msh392fb98c48f0737p12839fjsn2546ba7e6d41",
	    "X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

def recipe_search(input):
    url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"
    querystring = {"query": {input}}
    headers = {
        "X-RapidAPI-Key": "9a22f3cf69msh392fb98c48f0737p12839fjsn2546ba7e6d41",
        "X-RapidAPI-Host": "recipe-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)
