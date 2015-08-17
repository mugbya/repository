from django.test import TestCase

import requests

# Create your tests here.

# payload = {
#     'client_id': 'dd90d6225d6bb60bf7a5',
#     'redirect_uri': 'http://127.0.0.1:8000',
# }
#
# r = requests.post('https://github.com/login/oauth/authorize', params = payload)
#
# oo = r.json()

# print(type(oo))

# access_token_info = {"access_token":"cf3c2b8e1f1c48d6cea072cbcb6daf7ad719a174","token_type":"bearer","scope":""}
#
# print(type(access_token_info))
# access_token = access_token_info['access_token']
# print("access_token: " + access_token )


oo = {1 : 'github', 2: 'qq'}

print(oo[1])