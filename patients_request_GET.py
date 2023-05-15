import requests

url = "https://3hr2j3gquj.execute-api.us-east-1.amazonaws.com/prod/patients"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
