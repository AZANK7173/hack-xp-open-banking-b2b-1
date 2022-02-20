import requests

from typing import Text


class XpDataApi:
    @property
    def records_per_page(self):
        return 10

    def __init__(self, client_id: Text, client_secret: Text):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_access_code = None
        self.api_base_endpoint = "https://openapi.xpi.com.br/"

    def define_endpoint(self, endpoint: Text):
        return f"{self.api_base_endpoint}{endpoint}"

    def _get_access_code(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PostmanRuntime/7.26.8'
        }

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response_key = requests.post(self.define_endpoint('oauth2/v1/access-token'), headers=headers, data=data)

        if response_key.ok:
            self.api_access_code = response_key.json()['access_token']
        else:
            raise Exception(f"Was not possible to get access_token - {response_key.text}, {response_key.status_code}")

    def _get_request_data(self, endpoint: Text):
        if self.api_access_code is None:
            self._get_access_code()
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'Authorization': f"Bearer {self.api_access_code}"
        }
        response = requests.get(self.define_endpoint(endpoint), headers=headers)

        if response.ok:
            return response.json()
        else:
            self._get_access_code()
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'PostmanRuntime/7.26.8',
                'Authorization': f"Bearer {self.api_access_code}"
            }
            response = requests.get(self.define_endpoint(endpoint), headers=headers)
            if response.ok:
                return response.json()
            else:
                raise Exception(f"Was not possible to get data. URL: {endpoint}")

    def get_broker_products(self):
        return self._get_request_data("broker/products")

    def get_broker_user_suitability(self, user_name: Text):
        return self._get_request_data(f"broker/{user_name}/suitability")

    def get_openbanking_user_data(self, user_name: Text):
        return self._get_request_data(f"openbanking/users/{user_name}")

    def get_openbanking_users_data(self):
        data_users = []
        data_page = [1]
        page_num = 0
        while data_page: #Cuidado para loop infinito
            params = f"limit={self.records_per_page}&offset={self.records_per_page*page_num}"
            data_page = self._get_request_data(f"openbanking/users?{params}")
            data_users.extend(data_page)
            page_num += 1
        return data_users

    def get_banking_user_account_balance(self, user_name: Text):
        return self._get_request_data(f"banking/users/{user_name}/checking-account/balance")

    def get_banking_user_account(self, user_name: Text):
        return self._get_request_data(f"banking/users/{user_name}/checking-account")

    def get_banking_user_investments(self, user_name: Text):
        return self._get_request_data(f"banking/users/{user_name}/investments")


if __name__ == '__main__':
    import os

    client_id = os.environ.get('HACK_XP_CLIENT_ID')
    client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
    api = XpDataApi(client_id=client_id, client_secret=client_secret)

    data = api.get_openbanking_users_data()

    print(len(data))



