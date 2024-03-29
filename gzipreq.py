import requests
import gzip
import json

url = 'http://localhost:8000/gzip'

data = {'some-felipe-key': 'some-felipe-value'}

compressed_data = gzip.compress(bytes('some-felipe-key', 'utf-8'))

# response = requests.post(url, headers={'Accept-Encoding': 'gzip'}, data=compressed_data)
response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
# response  = requests.post(
#     url, headers={'Content-Type': 'application/json', 'x-test': 'x-error'}, data=json.dumps(data)
# )

print(response.text)
