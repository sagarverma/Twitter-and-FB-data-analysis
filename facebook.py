import requests

url = "https://graph.facebook.com/"
ID = "CERCatIIITD/feed"
ACCESS_TOKEN = "CAACEdEose0cBAGiDWvlIQsDLUaC2nD7nZB1vpYfRZC3SzTUGHK3NZA4QwKOBpqpYLo8BWGAhrWUu9QRE2DZBfXxV5NF6CjtpH6NvPI3kbAmXgBokFOzSSPxZCiNgZAbLSvrwgz0WN9C9UhbBf1wIZCcyluZAcvNiE0XlZASDt67I27KCjvqUc4hSpWykmZCavZBC3lOCVtnPaVZAZCgZDZD"
VERSION = "v2.0"

response = requests.get(url+VERSION+"/"+ID+"?access_token="+ACCESS_TOKEN)
#print type(response)
page_info = response.json()

print page_info