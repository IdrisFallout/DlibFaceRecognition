import urllib.request

url = "http://192.168.1.102:8080/shot.jpg"


def get_feed():
    response = urllib.request.urlopen(url)
    data = response.read()
    return data
