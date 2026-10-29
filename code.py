import requests
api_key =  "429f6b53-e78d-4ead-85fb-d1b80e033ee7"
classification_url = "https://api.harvardartmuseums.org/classification"

params={
    "apikey":api_key,
    "size":100
    
}

response =requests.get(classification_url,params)
print(response.status_code)

data=response.json()
for item in data ["records"]:
    print(item["name"])