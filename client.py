import requests

URL = 'http://127.0.0.1:5000'

# response = requests.post(f'{URL}/ad/',
#                          json={'header': 'Продаю запчасти на авто', 'description': 'Продам оптом и в розницу',
#                                'owner': 'User5'})
response = requests.get(f'{URL}/ad/4')
# response = requests.delete(f'{URL}/ad/4')


print(response)
print(response.status_code)
print(response.json())
