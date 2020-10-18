import requests

URL = "http://54.172.146.52/predict"

if __name__ == "__main__":

    test_text = "Jejeejje Jejeejje Jejeejje Jejeejje"
    values = {"text": test_text}
    response = requests.post(URL, json=values)
    data = response.json()

    print(data)