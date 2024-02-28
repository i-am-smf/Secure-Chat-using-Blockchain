from requests import get
import json
data=get("https://discord.com/api/guilds/796762525412360226/widget.json").json()

with open("test.json","w") as f:
    json.dump(data,f)
    f.close()