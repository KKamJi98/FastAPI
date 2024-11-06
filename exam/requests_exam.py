import requests


#########################################################
#########################################################

# r = requests.get("http://localhost:8000/header/hi/hello")
# print(r.json())

#########################################################
#########################################################

# url = "http://localhost:8000/items"
# data = {
#     "name": "Apple",
#     "price": 3.5
# }
# response = requests.post(url=url, json=data)
# print(response.json())

#########################################################
#########################################################

# url = "http://localhost:8000/hi"
# data = {
#     "who": "MOM"
# }
# response = requests.post(url=url, json=data)
# print(response.json())

#########################################################
#########################################################

url = "http://localhost:8000/agent"
response = requests.get(url=url)
print(response.json())
