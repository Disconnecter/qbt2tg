import requests
import config

qbittorrent_cookies = None

def qb_login():
    global qbittorrent_cookies
    url = f"{config.QBITTORRENT_URL}/api/v2/auth/login"
    data = {'username': config.QBITTORRENT_USERNAME, 'password': config.QBITTORRENT_PASSWORD}
    session = requests.Session()
    response = session.post(url, data=data)
    if response.ok and response.text == 'Ok.':
        qbittorrent_cookies = session.cookies
    else:
        qbittorrent_cookies = None

def qb_api(path, method='get', data=None, files=None):
    if qbittorrent_cookies is None:
        qb_login()
    url = f"{config.QBITTORRENT_URL}/api/v2/{path}"
    session = requests.Session()
    session.cookies = qbittorrent_cookies
    try:
        if method == 'get':
            resp = session.get(url)
        elif method == 'post':
            resp = session.post(url, data=data, files=files)
        else:
            raise Exception("Unsupported method")
        if resp.status_code == 403:
            qb_login()
            session.cookies = qbittorrent_cookies
            if method == 'get':
                resp = session.get(url)
            else:
                resp = session.post(url, data=data, files=files)
        return resp
    except Exception as e:
        print(f"API error: {e}")
        return None

def get_all_torrents():
    resp = qb_api('torrents/info')
    return resp.json() if resp and resp.ok else []

def get_categories():
    resp = qb_api('torrents/categories')
    return resp.json() if resp and resp.ok else {}

def add_torrent(file_path, category=None):
    with open(file_path, 'rb') as f:
        files = {'torrents': f}
        data = {}
        if category:
            data['category'] = category
        resp = qb_api('torrents/add', method='post', data=data, files=files)
    return resp.ok if resp else False

def delete_torrent(hash_, delete_files=True):
    data = {'hashes': hash_, 'deleteFiles': str(delete_files).lower()}
    resp = qb_api('torrents/delete', method='post', data=data)
    return resp.ok if resp else False

def get_torrent_by_hash(hash_):
    torrents = get_all_torrents()
    for t in torrents:
        if t['hash'] == hash_:
            return t
    return None
