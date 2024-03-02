from requests import get
import json
# data=get("https://api.mozambiquehe.re/bridge?auth=6e17a1fff557ed62842e0339c07a70ff&player=Yeshwin MI&platform=PC").json()

headers={"Authorization":"c2ddee0a-0d58-4cfb-a89b-358d888ed798"}

accountId="REYAAN_3"

data=get(f"https://fortnite-api.com/v2/stats/br/v2/{accountId}",headers=headers).json()

with open("test.json","w") as f:
    json.dump(data,f)
    f.close()
