import json

dict={
    1:"smf",
    2:"rsa"
}

dump=json.dumps(dict)

print(type(dump))

dict2=json.loads(dump)

print(type(dict2))