# Exo cours 5

import requests
import json
import re

url = "https://open-medicaments.fr/api/v1/medicaments?query=paracetamol"
json_data = requests.get(url).text

data = json.loads(json_data)
result = []

for d in data:
    denomination = d['denomination']
    name = re.search('[A-Z]+ ', denomination).group(0).strip()
    brand = re.search(' [A-Z]+ ', denomination).group(0).strip()
    dosage = re.search(' [0-9]+ [a-z]+,', denomination).group(0)[:-1]
    med_type = re.search(', [a-zé]+', denomination).group(0)[2:]
    result.append([name, brand, dosage, med_type])

print(result)


