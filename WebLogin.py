import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

USER = "2018184020"
PASS = "1077111"

session = requests.session()

login_info = {
    "m_id": USER,
    "m_passwd": PASS
}

#POST로 데이터 보내기
url_login = "http://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl"
res = session.post(url_login, data=login_info)
res.raise_for_status() #오류 발생하면 예외 발생

url_mypage = "http://eclass.tukorea.ac.kr/ilos/main/main_form.acl"
res = session.get(url_mypage)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

