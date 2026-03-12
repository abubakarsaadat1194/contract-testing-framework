import requests

BASE_URL = "http://localhost:5000"


class UserClient:

    @staticmethod
    def get_user(user_id):

        url = f"{BASE_URL}/users/{user_id}"

        response = requests.get(url)

        return response