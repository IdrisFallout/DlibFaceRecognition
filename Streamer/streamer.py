import urllib.request

url = "http://102.166.27.192:8080/shot.jpg"


def get_feed():
    response = urllib.request.urlopen(url)
    data = response.read()
    return data
