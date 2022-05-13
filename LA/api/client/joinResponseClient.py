import requests
import json


def joinResponseClient(ip, port, device, context, keys):
    """
    payload = (
            '{"device":"'
            + str(device).replace("\'", "\"")
            + '","context":"'
            + str(context).replace("\'", "\"")
            + '", "keys": "'
            + str(keys).replace("\'", "\"")
            + '"}'
        )
    """
    # payload =json.loads(payload)
    payload = {"device": str(device), "context": str(context), "keys": str(keys)}

    # payload = json.dumps(payload)
    #print(payload)
    url = "http://" + ip + ":" + str(port) + "/api/joinresponse"

    headers = {
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, data=payload)
    #print(response.status_code)
