import requests
import pprint
APPID = 'your_appid'
def dishes_ingredients(ingredients):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    response = requests.get(url, params = {'ingredients' : ingredients, 'ranking' : 1, 'number' : 10}, headers = {'x-api-key' : APPID})
    return response.json()