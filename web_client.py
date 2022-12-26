import requests
r = requests.get('http://127.0.0.1:5000/users')
print(r.json())
r = requests.post('http://127.0.0.1:5000/users',
              json={"name": "Andrei", "surname": "Topor", "flat_quantity": "1"})
id_user_get = 1
r = requests.get(f'http://127.0.0.1:5000/users/{id_user_get}')
r = requests.get(f'http://127.0.0.1:5000/users/{id_user_get}/flat')
r = requests.post(f'http://127.0.0.1:5000/users/{id_user_get}/flat', json={"quality": "3", "area" : 75})

id_user_del = 2
r = requests.delete(f'http://127.0.0.1:5000/users/{id_user_del}')
