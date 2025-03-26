import requests
from config import BASE_URL, API_KEY


class BaseAPI:
    def __init__(self, base_url=BASE_URL, api_key=API_KEY):
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return response