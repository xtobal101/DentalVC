import requests

url = "https://3hr2j3gquj.execute-api.us-east-1.amazonaws.com/prod/patient"

payload = "{\r\n    \"patientId\" : \"103\",\r\n    \"patientName\" : \"bruno\"\r\n}"
headers = {
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


