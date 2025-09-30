from requests import get, delete

print(delete('http://localhost:8080/api/items/2_555').json())
