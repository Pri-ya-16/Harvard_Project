import requests

object_url = "https://api.harvardartmuseums.org/object"

classifications = [
    "Prints",
    "Paintings",
    "Drawings",
    "Coins",
    "Archival Material"
]

for classification in classifications:

    all_records = []
    page = 1

    print("\nCollecting:", classification)

    while len(all_records) < 2500:

        params = {
            "apikey":"************************************",
            "classification": classification,
            "size": 100,
            "page": page
        }

        response = requests.get(object_url, params=params)
    
        data = response.json()

        records = data.get("records", [])

        if len(records) == 0:
            break

        all_records.extend(records)
        all_records = all_records[:2500]

        print("Page:", page, "Records:", len(all_records))

        page += 1

    print("Finished:", classification)
    print("Total records:", len(all_records))