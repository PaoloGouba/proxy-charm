import requests
import json


def get_proxy_info(ip_address : str = '176.113.73.104') :
    
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
    
    return result


def get_proxy_location(ip_address : str = '176.113.73.104') -> str :
    
    result = get_proxy_info(ip_address)

    return result["country_code"]


