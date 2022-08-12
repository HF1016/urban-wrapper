import requests
import aiohttp
from .error import (
    TokenInvalid,
    UrbanException,
)





class Client:
    def __init__(self, token):
        self.token = token
        self.__url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        self.__headers = {
            "X-RapidAPI-Key": token,
            "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }
        self.check_token()
    def check_token(self):
        r = requests.request("GET", self.__url, headers=self.__headers, params={'term': 'test'})

        if r.status_code != 200:
            raise TokenInvalid("Invalid token")


    def define(self, term: str):
        params = {'term': term}
        r = requests.request("GET", self.__url, headers=self.__headers, params=params)
        if r.status_code == 200:
            response = r.json()
            return [] if len(response['list']) == 0 else response['list']
        elif r.status_code == 401:
            response = r.json()
            raise TokenInvalid(f"401 | {response['message']}")
        else:
            raise UrbanException(f"{r.status_code} | {r.text}")
        
class AsyncClient(Client):
    def __init__(self, token):
        super().__init__(token)
        self.__url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        self.__headers = {
            "X-RapidAPI-Key": token,
            "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }
    async def define(self, term: str):
        params = {'term': term}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url, headers=self.__headers, params=params) as r:
                if r.status == 200:
                    response = await r.json()
                    return [] if len(response['list']) == 0 else response['list']
                elif r.status == 401:
                    response = await r.json()
                    raise TokenInvalid(f"401 | {response['message']}")
                else:
                    raise UrbanException(f"{r.status} | {r.text}")
        