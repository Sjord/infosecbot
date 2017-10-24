import requests

def create_session():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Infosecbot https://github.com/Sjord/infosecbot'})
    return session

webclient = create_session()
