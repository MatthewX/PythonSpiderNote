from bs4 import BeautifulSoup
import requests
import configparser
from requests.auth import HTTPBasicAuth


def create_session():
    cf = configparser.ConfigParser()
    cf.read("Config.ini")
    cookies = cf.items("cookies")
    cookies = dict(cookies)
    email = cf.get("info", "email")
    password = cf.get("info", "password")
    # Setup data
    login_data = {"email": email, "password": password}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
            'Host': 'www.zhihu.com',
            'Referer': 'http://www.zhihu.com/'
    }
    # Login
    session = requests.session()
    response = session.post('https://www.zhihu.com/login/email', data=login_data, headers=headers)
    # If login is failing
    if response.json()["r"] == 1:
        print("Login fails, the reason is: " + response.json()["msg"])
        print("So we are gonna use cookies to login")
        has_cookies = False
        for key in cookies:
            if key != '__name__' and cookies[key] != '':
                has_cookies = True
                break
        if has_cookies is False:
            raise ValueError("Please fill the cookies in the Config.ini file")
        else:
            # Use cookies to login
            response = session.get('http://www.zhihu.com/login/email', cookies=cookies)
    # Write into the file
    file = open("content.txt", "w")
    file.write(response.text)
    file.close()
    return session, cookies


if __name__ == '__main__':
    requests_session, requests_cookies = create_session()
    url = 'http://www.zhihu.com/topic/19552832'
    content = requests_session.get(url, cookies=requests_cookies).text
    with open('url.html', 'w') as fp:
        fp.write(content)



