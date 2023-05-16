import requests

url = 'https://api.spacetraders.io/v2/register'

headers = {'Content-Type': 'application/json'}

data = {
    'symbol': 'Andrew',
    'faction': 'COSMIC'
}

response = requests.post(url, headers=headers, json=data)

#Write response to response.json
with open('response.json', 'w') as outfile:
    outfile.write(response.text)
