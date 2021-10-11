import json
import requests
import http.client
from json import JSONDecodeError, JSONEncoder
import logging

# from functions import AUTH_URL, AUTH_TOKEN
class GetAuthToken:
    def get_auth_token(self):
        """ Generates the authorization bearer test token for return_cause method """
        url = "https://accounts.spotify.com/api/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': "Basic NTU3YjIxZjFhMTY2NDZlOGEzNTgyZWE1YjVjODg3ZmI6NGY0M2YwZDBmZjEwNGUzZTliNWY0ZTZkMzdkYTU2NmE="}
        data = {"grant_type":"client_credentials"}
        
        try: 
            response = requests.post(url, headers=headers, data=data)
            auth_json = response.content
            auth_data = json.loads(auth_json)
            return auth_data['access_token']
        except (ConnectionError, JSONDecodeError, KeyError) as ex:
            logging.error('Exception occurred while getting the auth token')
            logging.error(ex)

token = GetAuthToken()
print(token.get_auth_token())