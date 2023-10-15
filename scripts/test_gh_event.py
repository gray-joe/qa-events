import requests

# Define the URL of your Flask application's /github route
url = 'http://0.0.0.0:5000/github'

# Define the JSON data you want to send as the request payload
payload = {
   "action": "opened",
   "issue": {
     "url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
     "number": 1347,
   },
   "repository" : {
     "id": 1296269,
     "full_name": "octocat/Hello-World",
     "owner": {
       "login": "octocat",
       "id": 1,
     },
   },
   "sender": {
     "login": "octocat",
     "id": 1,
   }
}

# Send a POST request to the /github route with the JSON payload
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    print('Event sent successfully.')
else:
    print(f'Failed to send event. Status code: {response.status_code}')
